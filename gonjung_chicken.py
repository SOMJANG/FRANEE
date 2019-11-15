import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import io
import base64

matplotlib.rcParams['font.family'] = "AppleGothic"
matplotlib.rcParams['figure.figsize'] = (35, 20)
matplotlib.rcParams['font.size'] = 20

# 크롤링해올 주소를 만들기 위한 dataIdx와 회사 상호명 Dictionary

dataIdx_dic = {"맘스터치": "70916", "BHC": "63110", "굽네치킨": "68742", "네네치킨": "63330", "BBQ": "61999", "멕시카나": "68643",
               "노랑통닭": "73398", "바른치킨": "66901", "부어치킨": "65480", "순수치킨": "72165", "처갓집": "70831",
               "호식이두마리치킨": "69732", "페리카나": "68748", "아웃닭": "57874", "땅땅치킨": "68220", "또래오래": "66885",
               "깐부치킨": "68508", "맥시칸치킨": "67269", "또봉이통닭": "66934", "지코바양념치킨": "69199", "디디치킨": "71598",
               "마파치킨": "66820", "훌랄라치킨": "62455", "오븐마루": "65757", "웰덤치킨": "61040"}


def makeCompanyInfoLink(inputString):
    search_link_format = "http://franchise.ftc.go.kr/user/extra/main/62/firMst/view/jsp/LayOutPage.do?dataIdx="
    search_link_format2 = "&spage=1&srow=10&column=brd&search="
    try:
        inputString = inputString.upper()
        dataIdx = dataIdx_dic[inputString]
        encodingName = requests.utils.quote(inputString)
        link = search_link_format + dataIdx + search_link_format2 + encodingName
    except:
        print("{}는 아직 서비스를 지원하지 않습니다.".format(inputString))
        link = "error"

    return link


def makeDataframeFromLink(link):
    dataframes_chicken = pd.read_html(link)
    make_df01 = makeCompanySummary(dataframes_chicken)
    make_df02 = makeCompanySalesInfo(dataframes_chicken)
    make_df03 = makeCompanyBrunchNumInfo(dataframes_chicken)
    make_df04 = makeCompanyBrunchNumChangeInfo(dataframes_chicken)
    make_df05 = makeCompanyPastSalesInfo(dataframes_chicken)
    make_df06 = makeADPrice(dataframes_chicken)
    make_df07 = makeBrunchBudamPrice(dataframes_chicken)
    make_df08 = makeContractDay(dataframes_chicken)
    make_df09 = makeInteriorPrice(dataframes_chicken)
    make_df10 = makeEmployeeInfo(dataframes_chicken)
    make_df11 = makeLowRecentThreeYears(dataframes_chicken)

    return [make_df01, make_df02, make_df03, make_df04, make_df05, make_df06, make_df07, make_df08, make_df09,
            make_df10, make_df11]


def makeCompanySummary(dataframes_chicken):
    data001 = dataframes_chicken[0].iloc[0:1, 0:4]
    for i in range(4):
        data001.iloc[0][i] = data001.iloc[0][i].replace('상호', '').replace(' ', '').replace('영업표지', '').replace('대표자',
                                                                                                               '').replace(
            '업종', '')
    data001T = data001.T
    data001T.columns = ['기업개요']
    data001T

    data002 = dataframes_chicken[0].iloc[2:3, 0:4]
    columns = list(dataframes_chicken[0].iloc[1:2, 0:4].iloc[0])
    data002.columns = columns
    data002T = data002.T
    data002T.columns = ['기업개요']
    data002T

    data003 = dataframes_chicken[0].iloc[4:5, 0:3]
    columns = list(dataframes_chicken[0].iloc[3:4, 0:3].iloc[0])
    data003.columns = columns
    data003T = data003.T
    data003T.columns = ['기업개요']
    data003T

    address = dataframes_chicken[1].T.iloc[1][0]
    splitaddress = address.split()

    postadress = splitaddress[2]
    postadress

    full_address = " ".join(splitaddress[3:-1]) + splitaddress[-1]
    full_address

    df_dic = {"기업개요": [full_address, postadress]}

    df_address = pd.DataFrame(df_dic)

    df_address.index = ['주소', '우편번호']

    df_address

    data_company_info_1 = data001T.append(data002T).append(data003T).append(df_address)

    return data_company_info_1


def makeCompanySalesInfo(dataframes_chicken):
    data0002 = dataframes_chicken[2].iloc[0:3, 1:7]
    index = list(dataframes_chicken[2].iloc[0:3, 0:1]['연도'])
    data0002.index = index
    data0002T = data0002.T
    return data0002T


def makeCompanyBrunchNumInfo(dataframes_chicken):
    gamengjum = dataframes_chicken[6].T
    columns = list(gamengjum.iloc[0:1, 0:18].iloc[0])

    gamengjum = dataframes_chicken[6].T.iloc[1:7, 0:18]

    gamengjum.columns = columns

    return gamengjum


def makeCompanyBrunchNumChangeInfo(dataframes_chicken):
    data007 = dataframes_chicken[7].iloc[0:3, 1:5]
    index = list(dataframes_chicken[7].iloc[0:3, 0:1]['연도'])
    data007.index = index

    return data007


def makeCompanyPastSalesInfo(dataframes_chicken):
    machulac = dataframes_chicken[8].T
    columns = list(machulac.iloc[0:1, 0:18].iloc[0])

    machulac = dataframes_chicken[8].T.iloc[1:10, 0:18]

    machulac.columns = columns

    machulac2 = machulac.T.fillna(0)
    return machulac2.T


def makeADPrice(dataframes_chicken):
    adPrice_df = dataframes_chicken[10].T
    adPrice_df.columns = ['광고정보']
    return adPrice_df


def makeBrunchBudamPrice(dataframes_chicken):
    df_budam = dataframes_chicken[13].T
    df_budam.columns = ['가맹점주 부담금 (천원)']
    return df_budam


def makeLowRecentThreeYears(dataframes_chicken):
    df_low = dataframes_chicken[12].T
    df_low.columns = ['최근 3년간 법 위반사실']
    return df_low


def makeInteriorPrice(dataframes_chicken):
    df_interior = dataframes_chicken[14].T
    df_interior.columns = ['인테리어 (천원)']
    return df_interior


def makeContractDay(dataframes_chicken):
    dataframes_chicken[15].columns = ['최초', '연장']
    dataframes_chicken[15].index = ["계약기간"]
    return dataframes_chicken[15].T


def makeEmployeeInfo(dataframes_chicken):
    data_employeeInfo = dataframes_chicken[3].T
    data_employeeInfo.columns = ['임원 / 직원 수']
    return data_employeeInfo


def makeChangeStoreNumGraph(dataframes):
    dataframes[3].plot.line(grid=True)


# plt.xticks(np.linspace(2015,2017,1))
# plt.xlim(2015, 2017)

def makeStoreGraph(dataframes):
    new_df = pd.DataFrame()
    year_info_1 = dataframes[2].index[0][0]
    year_info_2 = dataframes[2].index[3][0]
    new_df[year_info_2] = dataframes[2][0:9].iloc[3][1:18]
    new_df[year_info_1] = dataframes[2][0:9].iloc[0][1:18]
    graph01 = new_df.plot.bar(grid=True, width=0.7)
    graph01.set_title("{}/{} 직영점&가맹점 현황".format(year_info_2, year_info_1), size=20)
    graph01.set_xlabel("지역", size=20)
    graph01.set_ylabel("수", size=20)
    plt.xticks(rotation=45, size=17)
    plt.yticks(size=17)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    chart = 'data:image/png;base64,{}'.format(graph_url)

    return chart


#     plt.legend(["2016년", "2017년"])

def makeSalesInfoGraph(dataframes):
    new_df = pd.DataFrame()
    year_info = dataframes[4].index[0][0]
    new_df[year_info] = dataframes[4][0:3].iloc[1][1:18]
    graph01 = new_df.plot.bar(grid=True, width=0.7)
    graph01.set_title("{} 지역별 평균매출액".format(year_info), size=20)
    graph01.set_xlabel("지역", size=20)
    graph01.set_ylabel("평균매출액 (천원)", size=20)
    plt.xticks(rotation=45, size=17)
    plt.yticks(size=17)


#     plt.legend(["2018년"])

def makeStandardSalesInfoGraph(dataframes):
    new_df = pd.DataFrame()
    year_info = dataframes[4].index[0][0]
    new_df[year_info] = dataframes[4][0:3].iloc[2][1:18]
    graph01 = new_df.plot.bar(grid=True, width=0.7)
    graph01.set_title("{} 지역별 3.3m^2당 평균매출액".format(year_info), size=20)
    graph01.set_xlabel("지역", size=20)
    graph01.set_ylabel("평균매출액 (천원)", size=20)
    plt.xticks(rotation=45, size=17)
    plt.yticks(size=17)


#     plt.legend(["2018년"])

def searchAndMakeDataframe():
    inputString = input()
    link = makeCompanyInfoLink(inputString)
    if link != 'error':
        dataframes = makeDataframeFromLink(link)
    return dataframes


def MultisearchAndMakeDataframe():
    inputString = input()
    inputString = inputString.split()
    link01 = makeCompanyInfoLink(inputString[0])
    link02 = makeCompanyInfoLink(inputString[1])
    if link01 != 'error' and link02 != 'error':
        dataframes01 = makeDataframeFromLink(link01)
        dataframes02 = makeDataframeFromLink(link02)
    else:
        dataframes01 = ["Service is not offer"] * 8
        dataframes02 = ["Service is not offer"] * 8
    return [dataframes01, dataframes02]


def searchAndMakeDataframe2(inputString):
    link = makeCompanyInfoLink(inputString)
    if link != 'error':
        dataframes = makeDataframeFromLink(link)
    return dataframes


def MultisearchAndMakeDataframe2(inputString):
    inputString = inputString.split()
    link01 = makeCompanyInfoLink(inputString[0])
    link02 = makeCompanyInfoLink(inputString[1])
    if link01 != 'error' and link02 != 'error':
        dataframes01 = makeDataframeFromLink(link01)
        dataframes02 = makeDataframeFromLink(link02)
    else:
        dataframes01 = ["Service is not offer"] * 8
        dataframes02 = ["Service is not offer"] * 8
    return [dataframes01, dataframes02]

def testFunction():
    print("test")
def testFunction2():
    print("test2")
def testFunction3():
    print("test3")

def testFunction4():
    print("test")
