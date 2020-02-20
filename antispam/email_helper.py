import base64
import re
from email.header import decode_header
from html.entities import name2codepoint
from html.parser import HTMLParser

import chardet
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


class _HTMLToText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self._buf = []
        self.hide_output = False

    def handle_starttag(self, tag, attrs):
        if tag in ('p', 'br') and not self.hide_output:
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = True

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self._buf.append('\n')

    def handle_endtag(self, tag):
        if tag == 'p':
            self._buf.append('\n')
        elif tag in ('script', 'style'):
            self.hide_output = False

    def handle_data(self, text):
        if text and not self.hide_output:
            self._buf.append(re.sub(r'\s+', ' ', text))

    def handle_entityref(self, name):
        if name in name2codepoint and not self.hide_output:
            c = chr(name2codepoint[name])
            self._buf.append(c)

    def handle_charref(self, name):
        if not self.hide_output:
            n = int(name[1:], 16) if name.startswith('x') else int(name)
            self._buf.append(chr(n))

    def get_text(self):
        return re.sub(r' +', ' ', ''.join(self._buf))

def html_to_text(html):
    """
    Given a piece of HTML, return the plain text it contains.
    This handles entities and char refs, but not javascript and stylesheets.
    """
    parser = _HTMLToText()
    try:
        parser.feed(html)
        parser.close()
    except:  #HTMLParseError: No good replacement?
        pass
    return parser.get_text()


_COMMON_WORDS = [
    "a", "about", "above", "across", "after", "afterwards",
    "again", "all", "almost", "alone", "along", "already", "also",
    "although", "always", "am", "among", "amongst", "amoungst", "amount",
    "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway",
    "anywhere", "are", "as", "at", "be", "became", "because", "become","becomes",
    "becoming", "been", "before", "behind", "being", "beside", "besides", "between",
    "beyond", "both", "but", "by","can", "cannot", "cant", "could", "couldnt", "de",
    "describe", "do", "done", "each", "eg", "either", "else", "enough", "etc", "even",
    "ever", "every", "everyone", "everything", "everywhere", "except", "few", "find", "for",
    "found", "four", "from", "further", "get", "give", "go", "had", "has", "hasnt", "have",
    "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers",
    "herself", "him", "himself", "his", "how", "however", "i", "ie", "if", "in", "indeed",
    "is", "it", "its", "itself", "keep", "least", "less", "ltd", "made", "many", "may", "me",
    "meanwhile", "might", "mine", "more", "moreover", "most", "mostly", "much", "must", "my",
    "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nobody", "none",
    "noone", "nor", "nothing", "now", "nowhere", "of", "off", "often", "on", "once",
    "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves",
    "out", "over", "own", "part","perhaps", "please", "put", "rather", "re", "same", "see",
    "seem", "seemed", "seeming", "seems", "she", "should","since", "sincere","so", "some", "somehow",
    "someone", "something", "sometime", "sometimes", "somewhere", "still", "such",
    "take","than", "that", "the", "their", "them", "themselves", "then", "thence",
    "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these",
    "they", "this", "those", "though", "through", "throughout",
    "thru", "thus", "to", "together", "too", "toward", "towards", "under", "until",
    "up", "upon", "us", "very", "was", "we", "well", "were", "what", "whatever", "when",
    "whence", "whenever", "where", "whereafter", "whereas", "whereby",
    "wherein", "whereupon", "wherever", "whether", "which", "while", 
    "who", "whoever", "whom", "whose", "why", "will", "with",
    "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves"
]


class Email():

    def __init__(self, path):
        self.path = path
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()

        self.title = lines[0][8:]
        i = 1
        while re.match(r'\s\S+', lines[i]):
            self.title += lines[i]
            i += 1
        self.i = i
        self.content = ''.join(lines[i:]).split('\n')

        self._parse_email()

    def _parse_email(self):
        decoded_title = decode_header(self.title)
        self.encoding = None
        t = ""
        for txt, enc in decoded_title:
            if enc != None:
                self.encoding = {'x-sjis': 'shift-jis'}.get(enc, enc)
                t += txt.decode(self.encoding, errors='ignore')
            else:
                if not isinstance(txt, str):
                    txt = txt.decode()
                t += txt

        self.title = re.sub(r'\s', ' ', t.lower())

        if not self._parse_content_base64():
            if self.encoding:
                # self.content.decode(encoding)
                with open(self.path, 'rb') as f:
                    lines = f.readlines()[self.i:]
                content = b''.join(lines)
                self.content = content.decode(self.encoding, errors='ignore')

        if isinstance(self.content, list):
            self.content = ' '.join(self.content)

        self._parse_content_html()

        self.content = self.content.lower()

        self.content = re.sub('=3d|=0d|=0a', '', self.content)

        self.content_words = re.findall(r'\w+', self.content)
        self.title_words = re.findall(r'\w+:?', self.title)

        # ps = PorterStemmer()
        # self.content_words = [
        #     ps.stem(w) for w in self.content_words
        #     # if w not in _COMMON_WORDS
        # ]

        self.content = ' '.join(self.content_words)
        self.title = ' '.join(self.title_words)

    def _parse_content_base64(self):
        content = ''.join(self.content)
        _smol_cont = content[:min(36, len(content))]
        try:
            check_content = str(base64.b64encode(base64.b64decode(_smol_cont)))[2:-1]
        except:
            return False
        if _smol_cont == check_content:
            try:
                self.content = base64.b64decode(content)
            except:
                return False
            encoding = chardet.detect(self.content)["encoding"]
            if not encoding:
                return False
            else:
                self.encoding = encoding
            self.content = self.content.decode(encoding, errors='ignore')
            return True
        else:
            return False

    def _parse_content_html(self):
        self.content = html_to_text(self.content)
        return True

    def is_reply(self):
        return bool('re:' in self.title)

    # def get_content_en_words(self):
    #     return re.findall(r'\w+', self.content_en)

    # def get_title_en_words(self):
    #     return re.findall(r'\w+', self.title_en)
