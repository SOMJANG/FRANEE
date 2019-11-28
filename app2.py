from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import gonjung_chicken as gjck
import matplotlib.pyplot as plt
import io
import run_keras_server as myModel
import base64
import get_article_titles as gat


app = Flask(__name__) # 매개변수 __name__으로 새로운 플라스크 인스턴스를 초기화
# 현재 디레터리와 같은 위치에서 HTML템플릿(templates) 폴더를 찾습니다.

class HelloForm(Form):
    sayhello = TextAreaField('', [validators.DataRequired()])

@app.route('/')
def index():
    form = HelloForm(request.form)
    return render_template('firstapp.html', form=form)

@app.route('/hello', methods=['POST'])
def hello():
    form = HelloForm(request.form)
    if request.method == 'POST' and form.validate():
        name = request.form['sayhello']
        mydfs = gjck.searchAndMakeDataframe2(name)

        my_articles = gat.getArticleTitle_100_df(name)

        article_df = myModel.classification_article_pos_neg(my_articles)

        positive_df = article_df[0]

        negative_df = article_df[1]

        neutral_df = article_df[2]

        # positive_df = myModel.positive_df
        #
        # negative_df = myModel.negative_df
        #
        # neutral_df = myModel.neutrality_df


        img = io.BytesIO()
        mydfs[2].plot.bar()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        img2 = io.BytesIO()
        mydfs[1].T.plot.bar()
        plt.xticks(rotation=45)
        plt.savefig(img2, format='png')
        img2.seek(0)
        graph_url2 = base64.b64encode(img2.getvalue()).decode()
        plt.close()



        testChart = 'data:image/png;base64,{}'.format(graph_url)
        testChart2 = 'data:image/png;base64,{}'.format(graph_url2)
        testChart3 = gjck.makeStoreGraph(mydfs)


        testJsonData = mydfs[1].to_json(orient='records')
        print(testJsonData)
        return render_template('hello.html', name=name,
                               tables=[mydfs[0].to_html(classes='test1')], titles=mydfs[0].columns.values,
                               tables2=[mydfs[1].to_html(classes='test2')], titles2=mydfs[1].columns.values,
                               tables3=[mydfs[2].to_html(classes='test3')], titles3=mydfs[2].columns.values,
                               tables4=[mydfs[3].to_html(classes='data')], titles4=mydfs[3].columns.values,
                               tables5=[mydfs[4].to_html(classes='data')], titles5=mydfs[4].columns.values,
                               tables6=[mydfs[5].to_html(classes='data')], titles6=mydfs[5].columns.values,
                               tables7=[mydfs[6].to_html(classes='data')], titles7=mydfs[6].columns.values,
                               tables8=[mydfs[7].to_html(classes='data')], titles8=mydfs[7].columns.values,
                               tables9=[mydfs[8].to_html(classes='data')], titles9=mydfs[8].columns.values,
                               tables10=[mydfs[9].to_html(classes='data')], titles10=mydfs[9].columns.values,
                               tables11=[mydfs[10].to_html(classes='data')], titles11=mydfs[10].columns.values,
                               test_graph=testChart, test2_graph=testChart2, test3_graph=testChart3, json_test=testJsonData,
                               positive_article=[positive_df.to_html(classes='article_positive')],
                               negative_article=[negative_df.to_html(classes='article_negative')],
                               neutral_article=[neutral_df.to_html(classes='article_neutral')])#,
                               # graph=plt.show())
    return render_template('firstapp2.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)