import random
from config import USER_AGENTS

def get_header():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Accept-Encoding': 'gzip, deflate',
    }


def get_charset(resp):
    charset = get_encoding_from_headers(resp.headers)
    if not charset or charset == 'ISO-8859-1':
        charset = get_encodings_from_content(resp.text)
        if not charset:
            charset = 'utf-8'
        else:
            charset = charset[0]
    if charset.startswith('gb') or charset.startswith('GK'):
        charset = 'gbk'
    return charset
