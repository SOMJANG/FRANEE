from flask import Flask, render_template, request
from wtforms import Form, TextAreaField, validators
import gonjung_chicken as gjck
import getInfofromsqlite3 as mydb
import matplotlib.pyplot as plt
import io
import run_keras_server as myModel
import base64
import get_article_titles as gat


app = Flask(__name__) # 매개변수 __name__으로 새로운 플라스크 인스턴스를 초기화
# 현재 디레터리와 같은 위치에서 HTML템플릿(templates) 폴더를 찾습니다.
company=''
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
        company=request.form['sayhello']
        # mydfs = gjck.searchAndMakeDataframe2(name)

        summary_info = mydb.getSummaryInfoFromSqlite3DB(name)

        branch_info = mydb.getBranchInfoFromSqlite3DB(summary_info[2])

        money_info = mydb.getMoneyInfoFromSqlite3DB(summary_info[2])

        finan_info = mydb.getFinanInfoFromSqlite3DB(summary_info[2])

        sales_info = mydb.getSalesInfoFromSqlite3DB(summary_info[2])


        # testJsonData = mydfs[1].to_json(orient='records')
        # print(testJsonData)
        return render_template('FRANEE_firstpagehtml.html', name=name, summary_info=summary_info, branch_info=branch_info, money_info=money_info, finan_info=finan_info, sales_info=sales_info)
    return render_template('firstapp2.html', form=form)

@app.route('/secondpage')
def secondPage():
    my_articles = gat.getArticleTitle_100_df(company)

    article_df = myModel.classification_article_pos_neg(my_articles)

    positive_df = article_df[0]

    negative_df = article_df[1]

    neutral_df = article_df[2]

    return render_template('FRANEE_secondpagehtml.html', positive_article=[positive_df.to_html(classes='article_positive')],
                               negative_article=[negative_df.to_html(classes='article_negative')],
                               neutral_article=[neutral_df.to_html(classes='article_neutral')])



@app.route('/thirdpage')
def thirdPage():
    return render_template(('FRANEE_thirdpagehtml.html'))

@app.route('/fourthpage')
def fourthPage():
    return render_template(('FRANEE_fourthpagehtml.html'))

@app.route('/fifthpage')
def fifthPage():
    return render_template(('FRANEE_fifthpagehtml.html'))

@app.route('/sixthpage')
def sixthPage():
    return render_template(('FRANEE_sixthpagehtml.html'))

if __name__ == '__main__':
    app.run(debug=True)