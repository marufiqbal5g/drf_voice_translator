from deep_translator import GoogleTranslator


def bn_to_en(text):

    try:

        translated = GoogleTranslator(
            source='bn',
            target='en'
        ).translate(text)

        return translated

    except Exception as e:

        print("TRANSLATION ERROR:", e)

        return ""