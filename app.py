from flask import Flask,render_template,request,flash,redirect,url_for
from flask_cors import CORS,cross_origin
import os
app =Flask(__name__)
cors = CORS(app)

UPLOAD_FOLDER='/videos'

#첫화면
@app.route("/")
def home():
    return render_template('home.html') 

#동영상 업로드 버튼이 있는 두번째 화면 렌더링
@app.route('/second')
def video_analysis():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('/second'))
        file=request.files['video'] #html에서 보내는 이름
        if file.filename=='':
            flash('no select file')
            return redirect(url_for('/second'))
        if file:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
            return render_template('final.html')

#마지막 페이지 점수,피드백 그리고 추가적으로 그래프
@app.route('/third')
def func():
    return '완료'
        
    

if __name__=='__main__':
    app.run(host="127.0.0.1",port="5000")