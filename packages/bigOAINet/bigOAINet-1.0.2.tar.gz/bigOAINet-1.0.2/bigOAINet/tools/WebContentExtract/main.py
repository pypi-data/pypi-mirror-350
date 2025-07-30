from newspaper import Article
import mxupy as mu


def extract(url, language='zh'):

    article = Article(url, language, output_format='json')

    article.download()

    article.parse()

    return article.text


def extractToFile(url, language='zh', output_file=''):
    res = extract(url, language)
    mu.wirteAllText(output_file, res)
