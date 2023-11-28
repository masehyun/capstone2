from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_cors import CORS,cross_origin
import os
from werkzeug.utils import secure_filename
from model import model_f
import pymysql

db=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1234',
    db='golf',
    charset='utf8')
cursor=db.cursor()

app =Flask(__name__)
cors = CORS(app)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER='/uploads'

global_user_id=0

b=model_f()
print(len(b))
for i in range(len(b)):
    print(b[i])

#첫화면
@app.route("/")
def home():
    return render_template('index.html') 
#세번째 페이지 태스트
@app.route("/3")
def test():
    return render_template('index3.html')

@app.route("/fourth")
def fourth_page():
    return render_template('index4.html')
@app.route("/third")
def third_page():
    return render_template('index3.html')
#두번째페이지를 렌더링
@app.route("/login")
def second_page():#id 받기
    user_id=request.args.get('userid')
    session['user_id'] = user_id
    print('user_ID=',user_id)
    return render_template('index2.html') 

#두번째 화면에서 업로드 버튼을 누를때
@app.route('/upload',methods=['POST'])
def upload_file():
    if request.method=='POST':
        f=request.files['file']
        print(f.filename)
        
        user_id = session.get('user_id', None)
        print('user_ID=',user_id)
        
        f.save('./static/assets/img/'+user_id+f.filename)
        file_name=user_id+f.filename
        
        #딕셔너리 정의(모델에서 딕셔너리 형태로 받을예정)
        grade=dict()
        grade={'address':1,'takeback':174,'backswing':170,'top':1,'impact_eye':-1,'impact_knee':1,'impact_foot':1}
        
        #코멘트 리스트. 나중에 웹으로 값 전송
        comment=list() 

        #점수 리스트.
        sc=[20,40,60,80,90,100,10]
        
        #회차별 종합 스코어 저장값 xtotal 초기화
        xtotal=[0,0,0,0,0]
        
        #회차 리스트
        tryn=[0,0,0,0,0]
        
        #종합스코어 초기화
        total=0
        
        #코멘트 알고리즘, 점수는 50점일때 각이 일치하는걸 가정, 오차는 5
        for key,value in grade.items():
            if(key=='address'):
                if(value==-1):
                    comment.append('발의 각도가 좁아요 어깨만큼 넓혀주세요ㅜㅜ.')
                elif(value==1 ):
                    comment.append('어드레스의 발 사이의 거리가 좋아요^^.')
                    total+=1
                elif(value==0):
                    comment.append('발 사이의 거리가 너무 멀어요ㅜㅜ.')
          
                    
            elif(key=='takeback'): #채 수평(손목좌표)과 팔 쭉 펴진지 나중에
                if(value>=165):
                    comment.append('테이크 어웨이 구간에서 팔이 잘 펴졌어요ㅎㅎ')
                    total+=1
                elif(value<165):
                    comment.append('테이크 어웨이 구간에서 팔을 더 펴주세요ㅜㅜ')
                elif(value==-1):
                    comment.append(' ')  
                 
            #뱌ㅐㄱ스윙
            elif(key=='backswing'): 
                
                if(value>=155):
                    comment.append('백스윙 구간에서 팔이 잘 펴졌어요ㅎㅎ')
                    total+=1
                elif(value<155):
                    comment.append('백스윙 구간에서 팔을 더 펴주세요ㅜㅜ')
                elif(value==-1):
                    comment.append(' ')    
                   
            elif(key=='top'): #백스윙에서 팔 위치
                if(value==1):
                    comment.append('볼을 끝까지 보는 시선 좋아요^^.')
                    total+=1
                elif(value==0):
                    comment.append('임팩트에서 볼을 끝까지 봐야해요!.')
                elif(value==-1):
                    comment.append(' ')    
                    
            #임팩트
            #임팩트 시선
            elif(key=='impact_eye'):
                if(value==1):
                    comment.append('임팩트 시 시선처리 좋아요!')
                    total+=1
                elif(value==0):
                    comment.append('임팩트때 공을 끝까지 봐주세요!')
                elif(value==-1):
                    comment.append(' ')   
            
            #임펙트 무릎
            elif(key=='impact_knee'):
                if(value==1):
                    comment.append('좋아요!')
                    total+=1
                elif(value==0):
                    comment.append('임패트 시 무릎이 붙게 해주세요!')
                elif(value==-1):
                    comment.append(' ')           
                    
            #임펙트 발거리
            elif(key=='impact_foot'):
                if(value==-1):
                    comment.append('발의 각도가 좁아요 어깨만큼 넓혀주세요ㅜㅜ.')
                elif(value==1):
                    comment.append('어드레스의 발 사이의 거리가 좋아요^^.')
                    total+=1
                elif(value==0):
                    comment.append('발 사이의 거리가 너무 멀어요ㅜㅜ.')
        #넘기는 리스트 comment의 값은 총 7개
            # 어드레스 한개
            # 테이크어웨이 1개
            # 백스윙,백스윙탑 두개
            # 임팩트 3개
            
       
        
        for i in range(7):
            print(comment[i])
        
        # 데이터베이스에서 이전 코멘트 불러오기
        xcomment=list()
        SQL=f"""SELECT id FROM golf_data WHERE id={user_id};"""
        print(SQL)
        cursor.execute(SQL)
        x=cursor.fetchone()
        
        # 기존 데이터 있으면 새로 갱신
        if x:
            print("아이디 존재,갱신")
            SQL=f"""
            INSERT INTO id{user_id} (total) VALUES({total});"""
            print(SQL)
            cursor.execute(SQL)
            db.commit()
            
            
            
        #없으면 새로 추가
        else:
            print(f"유저 아이디 {user_id} 없음")
            SQL=f"""CREATE TABLE id{user_id}(
              cnt int AUTO_INCREMENT PRIMARY KEY,
              total int
            );"""
            print(SQL)
            cursor.execute(SQL)
            SQL=f"""INSERT INTO id{user_id}(total) VALUES({total});"""
            print(SQL)
            cursor.execute(SQL)
            SQL=f"""INSERT INTO golf_data(id) VALUES({user_id});"""
            print(SQL)
            cursor.execute(SQL)
            db.commit()
           
        
  
        SQL=f"""SELECT * FROM id{user_id} ORDER BY cnt DESC;"""
        cursor.execute(SQL)
        y=cursor.fetchmany(5)
        db.commit()
        db.close()
        
       
        
        if y:
           ly=list(y)
           print(ly[0])
           
           for i in range(len(ly)):
               
                print(ly[i][0])
                xtotal[len(ly)-i-1]=ly[i][1]
                tryn[len(ly)-i-1]=ly[i][0]
           print(xtotal)
           print(tryn)  
        
        
        
        #딕셔너리 값을 html로 넘김
        return render_template('index3.html',values=comment,xvalues=xtotal,tryn=tryn,file_name=file_name)
    else:
        return render_template('index2.html')
    
#마지막 페이지 점수,피드백 그리고 추가적으로 그래프
@app.route('/third')
def func():
    return '완료'
        
    

if __name__=='__main__':
    app.run(host="127.0.0.1",port="5000")