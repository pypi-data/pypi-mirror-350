import unicodedata


# get plain old ascii version of a string (remove fancy chars)
def asciiize_string(str):
    return unicodedata.normalize('NFKD', str).encode('ascii', 'ignore').decode('utf-8')


# retrieve a text obejct from localized texts collection with given preferred locale
def get_localized_text(texts, preferred_locale="en"):
    if len(texts) == 0:
        return None

    # lets convert the texts list into indexed dictionary
    indexed = {}
    for text in texts:
        indexed[text["locale"]] = text

    if preferred_locale in indexed:
        return indexed[preferred_locale]
    if "en" in indexed:
        return indexed["en"]

    return texts[0]  # if everything fails - return the first text


def get_localized_name(texts, preferred_locale="en"):
    text = get_localized_text(texts, preferred_locale)
    if text is None:
        return "??"
    return text["name"]
