# Google Colaboratory에서 실행할 ipynb 코드입니다.
# .py로 변경하며 오류나는 코드는 주석처리 하였으니 주석 해제 후 Google Colaboratory에서 실행할 것

# 셀레니움 설치 및 크롬 드라이버 생성

# 업데이트 및 설치
# !apt-get update
# !apt install chromium-chromedriver
# !pip install selenium

# 크롬드라이버 옵션 설정
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('window-size=1920x1080')
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
options.add_argument("lang=ko_KR")


# 옵션값을 속성으로 주는 크롬드라이버 객체 생성
driver = webdriver.Chrome('chromedriver',options=options)



# 파이썬에서 대기(waiting)를 하기 위해 사용되는 내부 모듈('time')
import time

# 정규식
import re

# css 대상 존재 유무를 is_displayed()로 찾는데 없을 때 에러가 뜨도록 불러온다
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import os, sys
# from google.colab import drive
# drive.mount('/content/mnt')
nb_path = '/content/notebooks'
os.symlink('/content/mnt/My Drive/Colab Notebooks', nb_path)
sys.path.insert(0, nb_path)

# cd /content/mnt/My Drive/Colab Notebooks

import requests
from bs4 import BeautifulSoup
from selenium import webdriver as wd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import re

options = Options()
options.add_argument('--no-sandbox')
keyword = "BHC"

url = "https://www.instagram.com/explore/tags/{}/".format(keyword)

instagram_tags = []
instagram_tag_dates = []

driver.get(url)
time.sleep(3)

driver.find_element_by_css_selector('div.v1Nh3.kIKUG._bz0w').click()
for i in range(2000):  # 크롤링할 태그 개수
    time.sleep(1)
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.C7I1f.X7jCj')))
        data = driver.find_element_by_css_selector('.C7I1f.X7jCj')  # C7I1f X7jCj
        tag_raw = data.text
        tags = re.findall('#[A-Za-z0-9가-힣]+', tag_raw)
        tag = ''.join(tags).replace("#", " ")  # "#" 제거

        tag_data = tag.split()

        for tag_one in tag_data:
            instagram_tags.append(tag_one)

        date = driver.find_element_by_css_selector("time._1o9PC.Nzb55")  # 날짜 선택
        date = date.get_attribute('datetime')
        date = re.sub('^[.]*', '', date)
        pattern = re.compile(r"(\d+)[-](\d+)[-](\d+)")
        match = re.search(pattern, date)
        new_date = match.group()
        instagram_tag_dates.append(new_date)

    except:
        instagram_tags.append("error")
        instagram_tag_dates.append('error')
    try:
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'a.HBoOv.coreSpriteRightPaginationArrow')))
        driver.find_element_by_css_selector('a.HBoOv.coreSpriteRightPaginationArrow').click()
    except:
        driver.close()

    time.sleep(3)
driver.close()

from collections import Counter

instagram_tag_dates.sort()
count = Counter(instagram_tags)
common_tag_10 = count.most_common(20)
count_date = Counter(instagram_tag_dates)
keys = list(count_date.keys())

myDic = {}

for i in range(len(keys)):
    myDic[keys[i]] = count_date[keys[i]]

import pandas as pd
mySeries = pd.Series(myDic)

import matplotlib.pyplot as plt
import matplotlib
# %matplotlib inline
matplotlib.rcParams['font.size'] = 20
matplotlib.rcParams['figure.figsize'] = (30, 20)
matplotlib.rcParams['font.family'] = "Malgun Gothic"

BHCDataFrame = pd.DataFrame()
BHCDataFrame['count'] = mySeries
BHCDataFrame.plot.bar(grid=True)
plt.title('nene', size = 40)
plt.xticks(rotation=45)

import datetime

now = datetime.datetime.now()
nowDate = now.strftime('%Y-%m-%d')

def dftoCsv(my_title_df):
  try:
     my_title_df.to_csv((keyword+ nowDate +'.csv'), sep=',', na_rep='NaN', encoding='euc-kr')
  except:
    print("Error")

dftoCsv(BHCDataFrame)
