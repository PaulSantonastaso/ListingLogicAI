"""
neighborhood_service.py

Fetches hyper-local neighborhood data for a property address.
Used to enrich MLS descriptions and generate Neighborhood Insight sections.

Uses the Places API New (v1) — not the legacy Nearby Search.
  Endpoint: places.googleapis.com/v1/places:searchNearby
  rankPreference=POPULARITY surfaces places people actually go to.

Two API calls per listing run:
  1. Google Geocoding API  — address → lat/lng (~$0.005/call)
  2. Places API New        — lat/lng → nearby places per category (~$0.032/call)

Total cost: ~$0.037 per listing run.
First 5,000 calls/month free on both APIs.

Failure handling:
  All failures are silent — returns None or empty list.
  Never raises. Never breaks the pipeline.

Place categories (fetched separately, top 3 each by popularity):
  coffee_shop, park, bakery, restaurant, supermarket,
  yoga_studio, pilates_studio, farmers_market

No blocklist — the LLM handles curation.
No schools, churches, hospitals, or demographic indicators.
"""

import asyncio
import logging
from dataclasses import dataclass

import httpx

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

GEOCODING_URL = "https://maps.googleapis.com/maps/api/geocode/json"
PLACES_NEARBY_URL = "https://places.googleapis.com/v1/places:searchNearby"

SEARCH_RADIUS_METERS = 1609  # 1 mile

INCLUDED_TYPES = [
    "coffee_shop",
    "park",
    "bakery",
    "restaurant",
    "supermarket",
    "yoga_studio",
    "pilates_studio",
    "farmers_market",
]

MAX_PLACES_PER_TYPE = 3   # top 3 per category by popularity
MAX_TOTAL_PLACES = 24     # 8 categories × 3 — LLM selects 3-5 from these


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class NearbyPlace:
    name: str
    place_type: str
    vicinity: str
    rating: float | None
    review_count: int | None


@dataclass
class NeighborhoodContext:
    address: str
    lat: float
    lng: float
    places: list[NearbyPlace]

    def has_content(self) -> bool:
        return len(self.places) > 0

    def format_for_prompt(self) -> str:
        """Format places list for injection into the LLM prompt."""
        if not self.places:
            return ""

        lines = [f"Nearby places within 1 mile of {self.address}:"]
        for place in self.places:
            rating_str = f", rated {place.rating}" if place.rating else ""
            reviews_str = f", {place.review_count} reviews" if place.review_count else ""
            lines.append(f"  - {place.name} [{place.place_type}]{rating_str}{reviews_str}")

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Geocoding
# ---------------------------------------------------------------------------

async def geocode_address(address: str, api_key: str) -> tuple[float, float] | None:
    """
    Convert a property address to lat/lng coordinates.
    Returns (lat, lng) or None if geocoding fails.
    """
    if not address or not address.strip():
        return None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GEOCODING_URL,
                params={
                    "address": address,
                    "key": api_key,
                },
                timeout=8.0,
            )

        data = response.json()

        if data.get("status") != "OK":
            print(f"[GEOCODING] Status: {data.get('status')}, Error: {data.get('error_message', 'none')}")
            return None

        results = data.get("results", [])
        if not results:
            return None

        location = results[0]["geometry"]["location"]
        return location["lat"], location["lng"]

    except Exception as e:
        logger.info(f"Geocoding failed for {address}: {e}")
        return None


# ---------------------------------------------------------------------------
# Places Nearby Search (Places API New)
# ---------------------------------------------------------------------------

async def _fetch_places_for_type(
    lat: float,
    lng: float,
    place_type: str,
    api_key: str,
    client: httpx.AsyncClient,
) -> list[NearbyPlace]:
    """Fetch top places for a single place type using Places API New."""
    try:
        response = await client.post(
            PLACES_NEARBY_URL,
            headers={
                "Content-Type": "application/json",
                "X-Goog-Api-Key": api_key,
                "X-Goog-FieldMask": "places.displayName,places.types,places.formattedAddress,places.rating,places.userRatingCount",
            },
            json={
                "includedTypes": [place_type],
                "maxResultCount": MAX_PLACES_PER_TYPE,
                "rankPreference": "POPULARITY",
                "locationRestriction": {
                    "circle": {
                        "center": {"latitude": lat, "longitude": lng},
                        "radius": float(SEARCH_RADIUS_METERS),
                    }
                },
            },
            timeout=8.0,
        )

        data = response.json()

        places = []
        for result in data.get("places", []):
            name = result.get("displayName", {}).get("text", "")
            if not name:
                continue

            places.append(NearbyPlace(
                name=name,
                place_type=place_type,
                vicinity=result.get("formattedAddress", ""),
                rating=result.get("rating"),
                review_count=result.get("userRatingCount"),
            ))

        return places

    except Exception as e:
        logger.info(f"Places fetch failed for type {place_type}: {e}")
        return []


async def get_neighborhood_places(
    lat: float,
    lng: float,
    api_key: str,
) -> list[NearbyPlace]:
    """
    Fetch nearby places of interest for a lat/lng coordinate.
    Runs all place type queries concurrently via Places API New.
    Returns up to MAX_TOTAL_PLACES results for LLM curation.
    """
    try:
        async with httpx.AsyncClient() as client:
            tasks = [
                _fetch_places_for_type(lat, lng, place_type, api_key, client)
                for place_type in INCLUDED_TYPES
            ]
            results = await asyncio.gather(*tasks)

        # Flatten and deduplicate by name
        seen_names: set[str] = set()
        places: list[NearbyPlace] = []

        for place_list in results:
            for place in place_list:
                if place.name.lower() not in seen_names:
                    seen_names.add(place.name.lower())
                    places.append(place)

                if len(places) >= MAX_TOTAL_PLACES:
                    break

            if len(places) >= MAX_TOTAL_PLACES:
                break

        return places

    except Exception as e:
        logger.info(f"Neighborhood places fetch failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

async def build_neighborhood_context(
    address: str | None,
    api_key: str | None,
) -> NeighborhoodContext | None:
    """
    Full neighborhood enrichment pipeline.
    Geocodes the address, fetches nearby places, returns NeighborhoodContext.

    Returns None if:
      - address is missing or incomplete
      - API key is not configured
      - geocoding fails
      - no interesting places found

    Never raises. Caller should check return value before using.
    """
    if not api_key:
        logger.info("GOOGLE_PLACES_API_KEY not set — skipping neighborhood enrichment")
        return None

    if not address or len(address.strip()) < 10:
        logger.info("Address too short or missing — skipping neighborhood enrichment")
        return None

    coords = await geocode_address(address, api_key)
    print(f"[NEIGHBORHOOD] Geocoding result for '{address}': {coords}")
    if not coords:
        logger.info(f"Could not geocode address: {address} — skipping neighborhood enrichment")
        return None

    lat, lng = coords
    places = await get_neighborhood_places(lat, lng, api_key)

    context = NeighborhoodContext(
        address=address,
        lat=lat,
        lng=lng,
        places=places,
    )

    if not context.has_content():
        logger.info(f"No interesting nearby places found for {address}")
        return None

    print(f"[NEIGHBORHOOD] Places found: {len(places)} — {[p.name for p in places]}")
    logger.info(f"Neighborhood context built for {address}: {len(places)} places found")
    return context