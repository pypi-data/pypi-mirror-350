import re
import unicodedata


class LLMTextCleaner:
    """Text cleaner specifically designed for LLM outputs"""
    
    def __init__(self):
        # Common problematic characters in LLM outputs
        self.char_replacements = {
            # Smart quotes
            '"': '"', '"': '"', ''': "'", ''': "'",
            # Dashes
            '–': '-', '—': '-', '―': '-',
            # Spaces
            '\xa0': ' ',  # Non-breaking space
            '\u2009': ' ',  # Thin space
            '\u200b': '',   # Zero-width space
            # Ellipsis
            '…': '...',
            # Other common issues
            '\ufeff': '',   # BOM
            '\u200c': '',   # Zero-width non-joiner
            '\u200d': '',   # Zero-width joiner
        }
    
    def clean(self, text):
        """Clean text by removing/replacing problematic characters"""
        if not text:
            return text
        
        # Apply character replacements
        cleaned = self._replace_characters(text)
        
        # Normalize Unicode
        cleaned = self._normalize_unicode(cleaned)
        
        # Fix common LLM formatting issues
        cleaned = self._fix_formatting_issues(cleaned)
        
        # Clean up whitespace
        cleaned = self._normalize_whitespace(cleaned)
        
        return cleaned
    
    def _replace_characters(self, text):
        """Replace problematic characters with clean equivalents"""
        for old_char, new_char in self.char_replacements.items():
            text = text.replace(old_char, new_char)
        return text
    
    def _normalize_unicode(self, text):
        """Normalize Unicode characters to ASCII equivalents where possible"""
        result = []
        
        for char in text:
            # Keep basic ASCII characters
            if ord(char) <= 127:
                result.append(char)
                continue
            
            # Try to decompose and get ASCII equivalent
            try:
                # Normalize to decomposed form
                decomposed = unicodedata.normalize('NFD', char)
                # Remove combining characters and keep base character
                ascii_char = ''.join(c for c in decomposed if unicodedata.category(c) != 'Mn')
                
                # If we got a valid ASCII character, use it
                if ascii_char and all(ord(c) <= 127 for c in ascii_char):
                    result.append(ascii_char)
                else:
                    # For non-convertible characters, check if they're printable
                    if char.isprintable() and unicodedata.category(char)[0] in 'LNPS':
                        result.append(char)
                    # Otherwise, skip the character
            except:
                # If normalization fails, keep printable characters
                if char.isprintable():
                    result.append(char)
        
        return ''.join(result)
    
    def _fix_formatting_issues(self, text):
        """Fix common LLM formatting issues"""
        # Remove excessive line breaks
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Fix spaced punctuation (common in some LLM outputs)
        text = re.sub(r'\s+([,.!?;:])', r'\1', text)
        
        # Fix missing spaces after punctuation
        text = re.sub(r'([,.!?;:])([A-Za-z])', r'\1 \2', text)
        
        # Remove extra spaces around parentheses
        text = re.sub(r'\s*\(\s*', ' (', text)
        text = re.sub(r'\s*\)\s*', ') ', text)
        
        # Fix common markdown artifacts that might remain
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)  # Remove bold
        text = re.sub(r'\*(.+?)\*', r'\1', text)      # Remove italic
        text = re.sub(r'`(.+?)`', r'\1', text)        # Remove code formatting
        
        return text
    
    def _normalize_whitespace(self, text):
        """Normalize whitespace while preserving paragraph breaks"""
        # Replace multiple spaces with single space
        text = re.sub(r'[ \t]+', ' ', text)
        
        # Normalize line endings to \n
        text = re.sub(r'\r\n|\r', '\n', text)
        
        # Remove trailing spaces from lines
        text = re.sub(r'[ \t]+\n', '\n', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text