from models.property_data import PropertyDetails


def _clean_list(items: list[str] | None) -> list[str]:
    if not items:
        return []

    cleaned = [item.strip() for item in items if item and item.strip()]
    return list(dict.fromkeys(cleaned))


def _normalize_phrase(value: str) -> str:
    text = value.strip().lower()

    replacements = {
        "stainless appliances": "stainless steel appliances",
        "stainless steel appliance package": "stainless steel appliances",
        "driveway parking": "driveway",
        "attached garage parking": "attached garage",
        "screened pool": "screened-in pool",
        "screened pool enclosure": "screened-in pool",
    }

    return replacements.get(text, value.strip())


def _normalize_list(items: list[str] | None) -> list[str]:
    cleaned = [_normalize_phrase(item) for item in (items or [])]
    return _clean_list(cleaned)


def normalize_property_details(details: PropertyDetails) -> PropertyDetails:
    details.key_features = _normalize_list(details.key_features)
    details.interior_features = _normalize_list(details.interior_features)
    details.exterior_features = _normalize_list(details.exterior_features)
    details.appliances = _normalize_list(details.appliances)
    details.pool_features = _normalize_list(details.pool_features)
    details.parking_features = _normalize_list(details.parking_features)

    if hasattr(details, "community_features"):
        details.community_features = _normalize_list(details.community_features)

    # Route misplaced community amenities out of private property fields
    community_terms = {
        "community pool",
        "playground",
        "fitness center",
        "clubhouse",
        "gated entry",
        "community clubhouse",
    }

    moved_to_community: list[str] = []

    for field_name in ["pool_features", "exterior_features", "key_features"]:
        values = getattr(details, field_name, [])
        kept = []

        for value in values:
            if value.strip().lower() in community_terms:
                moved_to_community.append(value)
            else:
                kept.append(value)

        setattr(details, field_name, kept)

    if hasattr(details, "community_features"):
        details.community_features = _clean_list(
            (details.community_features or []) + moved_to_community
        )

    # Route appliance-like terms into appliances
    appliance_terms = {
        "stainless steel appliances",
        "dishwasher",
        "microwave",
        "range",
        "oven",
        "refrigerator",
    }

    moved_to_appliances: list[str] = []

    for field_name in ["key_features", "interior_features"]:
        values = getattr(details, field_name, [])
        kept = []

        for value in values:
            if value.strip().lower() in appliance_terms:
                moved_to_appliances.append(value)
            else:
                kept.append(value)

        setattr(details, field_name, kept)

    details.appliances = _clean_list((details.appliances or []) + moved_to_appliances)

    return details