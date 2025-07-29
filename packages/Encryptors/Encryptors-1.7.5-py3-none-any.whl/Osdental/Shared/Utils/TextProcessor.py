import re

class TextProcessor:
    
    @staticmethod
    def to_lower(text: str) -> str:
        return text.lower()

    @staticmethod
    def to_upper(text: str) -> str:
        return text.upper()

    @staticmethod
    def capitalize(text: str) -> str:
        return text.capitalize()

    @staticmethod
    def title_case(text: str) -> str:
        return text.title()
    
    @staticmethod
    def is_numeric(text: str) -> bool:
        return text.isdigit()

    @staticmethod
    def is_alpha(text: str) -> bool:
        return text.isalpha()

    @staticmethod
    def remove_whitespace(text: str) -> str:
        return ' '.join(text.split())

    @staticmethod
    def remove_special_chars(text: str, allowed: str = '') -> str:
        return re.sub(fr'[^\w\s{re.escape(allowed)}]', '', text)
    
    @staticmethod
    def concatenate(*parts: str, sep: str = ' ') -> str:
        return sep.join(parts)
    
    @staticmethod
    def contains(text: str, sub: str, case_sensitive: bool = True) -> bool:
        return sub in text if case_sensitive else sub.lower() in text.lower()
    
    @staticmethod
    def clean_str(text:str):
        text = text.lower()
        text = text.strip()
        text = re.sub(r'\s+', '_', text)
        text = re.sub(r'[^a-z0-9 ]', '', text)
        return text

    @staticmethod
    def remove_prefix(text: str, prefix: str) -> str:
        return text[len(prefix):] if text.startswith(prefix) else text

    @staticmethod
    def remove_suffix(text: str, suffix: str) -> str:
        return text[:-len(suffix)] if text.endswith(suffix) else text
    

    @staticmethod
    def truncate(text: str, length: int, ellipsis: bool = False) -> str:
        return text[:length] + ('...' if ellipsis and len(text) > length else "")
    

    @staticmethod
    def slugify(text: str) -> str:
        text = TextProcessor.normalize(text)
        text = re.sub(r"[^\w\s-]", "", text).strip().lower()
        return re.sub(r"[-\s]+", "-", text)
    
