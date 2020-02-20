from antispam.email_helper import Email
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def test_errs():
    dirs = [
        '/Users/ionutcosmin/Documents/antispam/lot1/train/Clean',
        '/Users/ionutcosmin/Documents/antispam/lot1/train/Spam'
    ]

    errs = 0
    total = 0

    for d in dirs:
        for f in os.scandir(d):
            total += 1
            try:
                e = Email(f.path)
            except Exception as exc:
                errs += 1
                print(f.path, "\t", exc, "\t", e.title)

    print("Errs: ", errs)


def single_test():
    e = Email('/Users/ionutcosmin/Documents/antispam/lot1/train/Clean/15b0bd4e3ae854fba7599ff133f48876')
    print(e.content)
    print(e.get_content_words())


def plot_single():
    pth = '/Users/ionutcosmin/Documents/antispam/lot1/train/Spam/2d662cc98d75860688cc654919ccbd46'
    print(pth)
    exit()
    e = Email(pth)
    words = e.get_content_words()
    words = e.content
    wc = WordCloud(width=512, height=512).generate(words)

    plt.figure(figsize=(10, 8), facecolor='k')
    plt.imshow(wc)
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.show()

plot_single()
