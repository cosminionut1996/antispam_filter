from antispam.email_helper import Email
from wordcloud import WordCloud
import sys
import os
import matplotlib.pyplot as plt
import shutil

try:
    folder = sys.argv[1]
except IndexError:
    print("usage: test_word_distribution folder")
    exit(0)


words = list()
for f in os.scandir(folder):
    email = Email(f.path)
    new_words = email.content_words

    if 'nwnw' in new_words:
            new_path = f.path.replace('train', 'awkward')
            # shutil.move(f.path, new_path)
            print(f.path)
    else:
        words += new_words

words = ' '.join(words)

wc = WordCloud(width=512, height=512).generate(words)
plt.figure(figsize=(10, 8), facecolor='k')
plt.imshow(wc)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()
