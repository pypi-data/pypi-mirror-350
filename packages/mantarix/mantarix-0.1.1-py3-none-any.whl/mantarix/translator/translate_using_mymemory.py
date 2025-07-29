import requests
import html

LANGUAGES_TO_CODES = {'afrikaans': 'af','albanian': 'sq','amharic': 'am','arabic': 'ar','armenian': 'hy','assamese': 'as','aymara': 'ay','azerbaijani': 'az','bambara': 'bm','basque': 'eu','belarusian': 'be','bengali': 'bn','bhojpuri': 'bho','bosnian': 'bs','bulgarian': 'bg','catalan': 'ca','cebuano': 'ceb','chichewa': 'ny','chinese_simplified': 'zh','chinese_traditional': 'zh','corsican': 'co','croatian': 'hr','czech': 'cs','danish': 'da','dhivehi': 'dv','dogri': 'doi','dutch': 'nl','english': 'en','esperanto': 'eo','estonian': 'et','ewe': 'ee','filipino': 'tl','finnish': 'fi','french': 'fr','frisian': 'fy','galician': 'gl','georgian': 'ka','german': 'de','greek': 'el','guarani': 'gn','gujarati': 'gu','haitian_creole': 'ht','hausa': 'ha','hawaiian': 'haw','hebrew': 'he','hindi': 'hi','hmong': 'hmn','hungarian': 'hu','icelandic': 'is','igbo': 'ig','ilocano': 'ilo','indonesian': 'id','irish': 'ga','italian': 'it','japanese': 'ja','javanese': 'jv','kannada': 'kn','kazakh': 'kk','khmer': 'km','kinyarwanda': 'rw','konkani': 'kok','korean': 'ko','krio': 'kri','kurdish_kurmanji': 'ku','kurdish_sorani': 'ckb','kyrgyz': 'ky','lao': 'lo','latin': 'la','latvian': 'lv','lingala': 'ln','lithuanian': 'lt','luganda': 'lg','luxembourgish': 'lb','macedonian': 'mk','maithili': 'mai','malagasy': 'mg','malay': 'ms','malayalam': 'ml','maltese': 'mt','maori': 'mi','marathi': 'mr','meiteilon_manipuri': 'mni','mizo': 'lus','mongolian': 'mn','myanmar': 'my','nepali': 'ne','norwegian': 'no','odia_oriya': 'or','oromo': 'om','pashto': 'ps','persian': 'fa','polish': 'pl','portuguese': 'pt','punjabi': 'pa','quechua': 'qu','romanian': 'ro','russian': 'ru','samoan': 'sm','sanskrit': 'sa','scots_gaelic': 'gd','sepedi': 'nso','serbian': 'sr','sesotho': 'st','shona': 'sn','sindhi': 'sd','sinhala': 'si','slovak': 'sk','slovenian': 'sl','somali': 'so','spanish': 'es','sundanese': 'su','swahili': 'sw','swedish': 'sv','tajik': 'tg','tamil': 'ta','tatar': 'tt','telugu': 'te','thai': 'th','tigrinya': 'ti','tsonga': 'ts','turkish': 'tr','turkmen': 'tk','twi': 'tw','ukrainian': 'uk','urdu': 'ur','uyghur': 'ug','uzbek': 'uz','vietnamese': 'vi','welsh': 'cy','xhosa': 'xh','yiddish': 'yi','yoruba': 'yo','zulu': 'zu'}

def translate(batch: list[str], source: str = "autodetect", target: str = "en") -> str:
    if not batch:
        return []
    arr = []
    for i, text in enumerate(batch):
        if not text.strip():
            continue
        base_url = "https://api.mymemory.translated.net/get"
        params = {
            "q": text,
            "langpair": f"{source}|{target}"
        }
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except:
            arr.append(text)
            continue
        data = response.json()
        if "responseData" in data and "translatedText" in data["responseData"]:
            translated_text = html.unescape(data["responseData"]["translatedText"])
        else:
            arr.append(text)
            continue
        arr.append(translated_text)
    return arr

def map_language_to_code(*languages):
    for language in languages:
        if language == "autodetect":
            yield language
        elif language in LANGUAGES_TO_CODES.keys():
            yield LANGUAGES_TO_CODES[language]
        else:
            raise Exception("language not found!")

def translate_using_mymemory(src:str, from_language:str, into_language:str):
    sents = []
    current_sent = ""
    num = 0
    for i in src:
        if num >= 250:
            sents.append(current_sent)
            current_sent = ""
            num = 0
        current_sent = current_sent + i
        num = num + 1
    sents.append(current_sent)
    from_language , into_language = map_language_to_code(from_language,into_language)
    res = translate(batch=sents,source=from_language,target=into_language)
    full_res = ""
    for i in res:
        if i == None:continue
        full_res = full_res + i
    return str(full_res)