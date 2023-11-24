import requests
import re
import html
import urllib.parse

# Detailed language list can be found here:  https://cloud.google.com/translate/docs/languages
# If you want to use auto-detect language, set source_language to 'auto'

class GoogleTranslate:
    # This function is used to initialize the class
    # Input: source_language - language to translate from
    #        target_language - language to translate to
    #        timeout - timeout for the request
    #output: None
    def __init__(self, source_language='auto', target_language='ru', timeout=5):
        self.source_language = source_language
        self.target_language = target_language
        self.timeout = timeout if timeout else 5
        self.pattern = r'(?s)class="(?:t0|result-container)">(.*?)<'
    
    # This function is used to make the request to Google Translate
    # Input: target_language - language to translate to
    #        source_language - language to translate from
    #        text - text to translate
    #        timeout - timeout for the request
    # Output: translated text or error message
    def make_request(self, target_language, source_language, text, timeout):
        escaped_text = urllib.parse.quote(text.encode('utf8'))
        url = 'https://translate.google.com/m?tl=%s&sl=%s&q=%s'%(target_language, source_language, escaped_text)
        response = requests.get(url, timeout=timeout if timeout else self.timeout)
        result = response.text.encode('utf8').decode('utf8')
        result = re.findall(self.pattern, result)
        if not result:
            f = open('error.txt')
            f.write(response.text)
            f.close()
            return('Произошла ошибка. Очень интересно, но ничего не понятно.')
        return html.unescape(result[0])
    
    # This function is used to translate the text
    # Input: text - text to translate
    #        target_language - language to translate to
    #        source_language - language to translate from
    #        timeout - timeout for the request
    # Output: translated text or error message
    def translate(self, text, target_language='', source_language='', timeout=''):
        if len(text) > 4096:
            return(f'Я не могу перевести этот текст! Вы ввели {len(text)} символов, это больше, чем 4096.')
        return self.make_request(target_language, source_language, text, timeout)

    # This function is used to translate the text from a file
    # Input: file_path - path to the file
    #        target_language - language to translate to
    #        source_language - language to translate from
    #        timeout - timeout for the request
    # Output: translated text or error message
    def translate_file(self, file_path, target_language='', source_language='', timeout=''):
        try:
            f = open(file_path)
            text = self.translate(f.read(), target_language, source_language, timeout)
            f.close()
            return text
        except Exception:
            return('Странно, не открывается...')