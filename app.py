from flask import Flask,render_template,request,flash,redirect,url_for
from flask_cors import CORS,cross_origin
import os
from model import model_f
app =Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER='/videos'

b=model_f()
print(len(b))
for i in range(len(b)):
    print(b[i])

#첫화면
@app.route("/")
def home():
    return render_template('index.html') 

#두번째페이지를 렌더링
@app.route("/second")
def second_page():
    return render_template('index2.html') 

#두번째 화면에서 업로드 버튼을 누를때
@app.route('/upload',methods=['GET','POST'])
def video_analysis():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file=request.files['video'] #html에서 보내는 이름
        if file.filename=='':
            flash('no select file')
            return redirect(request.url)
        if file:
            print("sdkfjsldkfj")
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            a=model_f()
            return render_template('index3.html')

#마지막 페이지 점수,피드백 그리고 추가적으로 그래프
@app.route('/third')
def func():
    return '완료'
        
    

if __name__=='__main__':
    app.run(host="127.0.0.1",port="5000")