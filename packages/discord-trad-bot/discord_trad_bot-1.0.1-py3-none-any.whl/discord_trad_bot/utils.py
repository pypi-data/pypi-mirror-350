import re
from googletrans import Translator

translator = Translator()

def preserve_user_mentions(text):
    """Replace user mentions with robust placeholders and return (text_with_placeholders, mention_map)."""
    mention_map = {}
    def mention_replacer(match):
        user_id = match.group(1)
        placeholder = f"[[[MENTION{len(mention_map)+1}]]]"
        mention_map[placeholder] = f"<@{user_id}>"
        return placeholder
    text_with_placeholders = re.sub(r'<@!?([0-9]+)>', mention_replacer, text)
    return text_with_placeholders, mention_map

def restore_mentions(text, mention_map):
    """Restore mentions in text using the mention_map (case-insensitive)."""
    for placeholder, mention in mention_map.items():
        text = re.sub(re.escape(placeholder), mention, text, flags=re.IGNORECASE)
    return text

def translate_message(content, dest_lang):
    """Translate content to dest_lang using googletrans."""
    return translator.translate(content, dest=dest_lang).text

def detect_language(content):
    """Detect the language of the content using googletrans."""
    try:
        detected = translator.detect(content)
        return detected.lang
    except Exception:
        return None 