from models.property_data import PropertyDetails
from models.property_image import PropertyImage
from models.feature_candidate import FeatureCandidate
from services.feature_router_service import route_image_features_to_structured_fields


HIGH_CONFIDENCE_THRESHOLD = 0.85


def normalize_feature(text: str) -> str:
    return text.strip().lower()


def merge_image_features_into_property(
    property_details: PropertyDetails,
    images: list[PropertyImage],
) -> PropertyDetails:
    """
    Merge high-confidence image features into PropertyDetails in three ways:

    1. Always → FeatureCandidate (for HITL panel display)
    2. If confidence >= 0.85 → key_features (for visual summary + MLS copy)
    3. If confidence >= 0.85 → structured PropertyDetails fields via feature
       router (for RESO CSV — appliances, interior_features, exterior_features,
       pool_features, parking_features)

    Never overwrites existing values. Only appends missing items.
    """

    existing_features = {
        normalize_feature(feature)
        for feature in property_details.key_features
    }

    merged_features = list(property_details.key_features)
    feature_candidates = list(property_details.feature_candidates)

    existing_candidate_keys = {
        (normalize_feature(candidate.name), candidate.source)
        for candidate in feature_candidates
    }

    for image in images:
        if image.metadata.likely_marketing_worthy is False:
            continue

        room_type = image.metadata.room_type

        for feature in image.visible_features:
            normalized = normalize_feature(feature.name)

            # --- Track 1: Always add to feature candidates for HITL panel ---
            if (normalized, "image") not in existing_candidate_keys:
                feature_candidates.append(
                    FeatureCandidate(
                        name=feature.name,
                        source="image",
                        confidence=feature.confidence,
                        confidence_level=feature.confidence_level,
                        evidence=f"Detected in image {image.filename} ({image.metadata.room_type})."
                    )
                )
                existing_candidate_keys.add((normalized, "image"))

            if feature.confidence < HIGH_CONFIDENCE_THRESHOLD:
                continue

            # --- Track 2: Add to key_features for MLS copy + visual summary ---
            if normalized not in existing_features:
                merged_features.append(feature.name)
                existing_features.add(normalized)

            # --- Track 3: Route into structured PropertyDetails fields ---
            property_details = route_image_features_to_structured_fields(
                property_details,
                feature,
                room_type,
            )

    property_details.images = images
    property_details.key_features = merged_features
    property_details.feature_candidates = feature_candidates

    return property_details