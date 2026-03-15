import re
import inflect

p = inflect.engine()

def normalize_variant_text(value: str) -> str:
    if not value:
        return ""

    value = value.strip().lower()
    value = re.sub(r"[^\w\s]", "", value)

    # convert plural to singular
    value = p.singular_noun(value) or value

    return value

    
# import re
# import inflect

# p = inflect.engine()

# def normalize_product_name(name: str) -> str:
#     name = name.strip().lower()

#     # remove punctuation
#     name = re.sub(r"[^\w\s]", "", name)

#     words = name.split()

#     # convert plurals to singular
#     words = [p.singular_noun(word) or word for word in words]

#     # sort so order doesn't matter
#     words.sort()

#     return " ".join(words)