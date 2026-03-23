from models.property_data import PropertyDetails
from models.property_image import PropertyImage
from models.feature_candidate import FeatureCandidate


HIGH_CONFIDENCE_THRESHOLD = 0.85


def normalize_feature(text: str) -> str:
    return text.strip().lower()


def merge_image_features_into_property(
    property_details: PropertyDetails,
    images: list[PropertyImage],
) -> PropertyDetails:
    """
    Merge high-confidence image features into PropertyDetails.key_features
    and store provenance in PropertyDetails.feature_candidates.
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

        for feature in image.visible_features:
            normalized = normalize_feature(feature.name)

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

            if normalized not in existing_features:
                merged_features.append(feature.name)
                existing_features.add(normalized)

    property_details.images = images
    property_details.key_features = merged_features
    property_details.feature_candidates = feature_candidates

    return property_details