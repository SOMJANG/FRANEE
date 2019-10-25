import requests
from bs4 import BeautifulSoup
import re
import pandas as pd


def getArticleTitle_100_df(search_word):
    label = [0] * 100

    my_title_dic = {"title": [], "link": [], "label": label}

    # search_word = "뉴욕증시"

    search_word_decoding = requests.utils.unquote(search_word)

    for i in range(10):
        num = i * 10 + 1

        url = "https://search.naver.com/search.naver?&where=news&query=" + search_word_decoding + "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=0&ds=&de=&docid=&nso=so:r,p:all,a:all&mynews=0&cluster_rank=23&start=" + str(
            num)

        req = requests.get(url)

        soup = BeautifulSoup(req.text, 'lxml')

        titles = soup.select("a._sp_each_title")

        links = soup.select("a._sp_each_title")

        for title in titles:
            title_data = title.text
            title_data = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…\"\“》]', '', title_data)
            my_title_dic['title'].append(title_data)

        for link in links:
            my_title_dic['link'].append(link.get('href'))

    my_title_df = pd.DataFrame(my_title_dic)

    return my_title_df