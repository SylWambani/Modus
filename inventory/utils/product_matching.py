from rapidfuzz import process, fuzz
from django.core.exceptions import ValidationError

def prevent_typo(new_value, existing_values, threshold=75):
    if not new_value or not existing_values:
        return

    match = process.extractOne(new_value, existing_values, scorer=fuzz.WRatio)

    if match:
        closest, score, _ = match

        if score >= threshold and new_value != closest:
            raise ValidationError(
                f"'{new_value}' looks like '{closest}'. "
                f"Please use the existing value."
            )


# from rapidfuzz import process, fuzz
# from django.core.exceptions import ValidationError

# def check_similar_products(name, existing_names, threshold=90):
#     match = process.extractOne(name, existing_names, scorer=fuzz.WRatio)

#     if match:
#         closest, score, _ = match

#         if score >= threshold:
#             raise ValidationError(
#                 f"A similar product '{closest}' already exists "
#                 f"(confidence {score:.0f}%)."
#             )