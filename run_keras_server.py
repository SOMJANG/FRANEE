from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
from konlpy.tag import Okt
import pickle

# tb._SYMBOLIC_SCOPE.value = False


# 1. 챗봇에 사용할 데이터 준비하기


test_data = pd.read_csv("./test_dataset_1007.csv")


def classification_article_pos_neg(test_data):
    okt = Okt()

    stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

    X_test = []
    # y_test = []

    for sentence in test_data['title']:
        temp_X = []
        temp_X = okt.morphs(sentence, stem=True)  # 토큰화
        temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
        X_test.append(temp_X)

    max_words = 35000
    max_len = 20

    with open('./tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    X_test = tokenizer.texts_to_sequences(X_test)

    # for i in range(len(test_data['label'])):
    #     if test_data['label'].iloc[i] == 1:
    #         y_test.append([0, 0, 1])
    #     elif test_data['label'].iloc[i] == 0:
    #         y_test.append([0, 1, 0])
    #     elif test_data['label'].iloc[i] == -1:
    #         y_test.append([1, 0, 0])
    #
    # # y_test = np.array(y_test)

    X_test = pad_sequences(X_test, maxlen=max_len)

    # 2. 모델 불러오기
    from keras.models import load_model

    model = load_model('./myClassifier1.h5')
    # print("\n 모델 정확도 : {:.2f}%".format(model.evaluate(X_test, y_test)[1] * 100))

    # 3. 모델 사용하기

    mypredict = model.predict(X_test)

    predict_labels = np.argmax(mypredict, axis=1)
    # original_labels = np.argmax(y_test, axis=1)

    titles = list(test_data['title'])
    # links = list(test_data['link'])

    mypredict_dic = {"title":titles,"label":predict_labels}

    myPredict_df = pd.DataFrame(mypredict_dic)

    positive_df = myPredict_df[myPredict_df['label'] == 2]

    negative_df = myPredict_df[myPredict_df['label'] == 0]

    neutrality_df = myPredict_df[myPredict_df['label'] == 1]

    return [positive_df, negative_df, neutrality_df]

