from flask import Flask,render_template,request,flash,redirect,url_for,session
from flask_cors import CORS,cross_origin
import os
from werkzeug.utils import secure_filename
from model import model_f
import pymysql
from Ground import pose_drawing
from input_slow import slowmotion

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
@app.route("/fourth")
def fourth_page():
    return render_template('index4.html',file_name=file_name,values=comment,problems=problem)
@app.route("/third")
def third_page():
    return render_template('index3.html',xvalues=xtotal,tryn=tryn,file_name=file_name,total=total,problems=problem)
@app.route("/fifth")
def fifth_page():
    return render_template('index5.html',file_name=file_name,values=comment,new_file_name=new_file_name,problems=problem)
@app.route("/sixth")
def sixth_page():
    return render_template('index6.html',file_name=file_name,values=comment,new_file_name=new_file_name,problems=problem)
@app.route("/seventh")
def seventh_page():
    return render_template('index7.html',file_name=file_name,values=comment,new_file_name=new_file_name,problems=problem)
@app.route("/eighth")
def eighth_page():
    return render_template('index8.html',file_name=file_name,values=comment,new_file_name=new_file_name,problems=problem)
@app.route("/ninth")
def ninth_page():
    return render_template('index9.html',file_name=file_name,values=comment,new_file_name=new_file_name,problems=problem)
    
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
    global comment,xtotal,tryn,file_name,new_file_name,total,problem
    if request.method=='POST':
        f=request.files['file']
        print(f.filename)
        
        user_id = session.get('user_id', None)
        print('user_ID=',user_id)
        
        f.save('./static/assets/img/'+user_id+f.filename)
        file_name=user_id+f.filename
        new_file_name='line'+user_id+f.filename
        print('save')
        
        
        #인공지능 모델 사용하기
        # video_path = './static/assets/img/'+file_name # 입력 동영상 파일 경로
        # output_path = './static/assets/img/'+new_file_name  # 출력 동영상(사용자에 줄 그은거) 파일 경로
       
        video_path = 'C:\\Users\\asdfg\\OneDrive\\바탕 화면\\올빼미\\static\\assets\\img\\'+file_name# 입력 동영상 파일 경로
        output_path = 'C:\\Users\\asdfg\\OneDrive\\바탕 화면\\올빼미\\static\\assets\\img\\'+new_file_name  # 출력 동영상(사용자에 줄 그은거) 파일 경로
        print(video_path)
        print(output_path)
        # 쭈현이꺼
        #video_path = "C:\\Users\\eju20\\OneDrive\\simulation\\pro_1.mp4"  # 입력 동영상 파일 경로
        #output_path = "C:\\Users\\eju20\\OneDrive\\simulation\\pro1_output.mp4"  # 출력 동영상 파일 경로
        #video_path = 'C:\\Users\\SAMSUNG\\Desktop\\CAPS\\static\\assets\\img\\'+file_name# 입력 동영상 파일 경로
        #output_path = 'C:\\Users\\SAMSUNG\\Desktop\\CAPS\\static\\assets\\img\\'+new_file_name  # 출력 동영상(사용자에 줄 그은거) 파일 경로
        #C:\\Users\\asdfg\\OneDrive\\바탕화면\\올빼미\\static\\assets\\img\\
        
        slow_path = slowmotion(video_path)
        grade=dict()
        print(grade)
        print("slowpath:", slow_path)
        
        print("outputpath:",output_path)
        grade=pose_drawing(slow_path, output_path)

        print('afterpose')
        #딕셔너리 정의(모델에서 받음)
        #코멘트 리스트. 나중에 웹으로 값 전송
        comment=list() 
        problem=list()

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
                    comment.append(["어드레스 시 어깨 폭 정도의 넓은 발 간격을 유지해야합니다.",
                                  '현재 발 간격에서 조금 더 넓게 유지해주세요.',
                                   '이런 올바른 발 간격을 유지하여야 스윙의 안정성과 균형이 향상됩니다.'])
                    problem.append('주 문제 ) 발 간격 좁음 문제')
                elif(value==1 ):
                    comment.append(['어드레스의 발 사이의 거리가 좋아요^^.',' ',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value==0):
                    comment.append(['어드레스 시 어깨 폭 정도의 발 간격을 유지해야합니다.',
                                   '현재 발 간격에서 조금 더 좁게 유지해주세요.',
                                   '이런 올바른 발 간격을 유지하여야 스윙의 안정성과 균형이 향상됩니다'])
                    problem.append('주 문제 ) 발 간격 넓음 문제')
          
                    
            elif(key=='takeback'): #채 수평(손목좌표)과 팔 쭉 펴진지 나중에
                if(value==1):
                    comment.append(['테이크 어웨이 구간에서 팔이 잘 펴졌어요',' ',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value<=165):
                    comment.append(['테이크어웨이 시 팔이 구부러져 있습니다.',
                    '팔의 각도가 좁으면 스윙 동작이 제한되어 힘 전달이 어렵습니다.',
                    '팔을 조금 더 펴준다면 스윙의 흐름이 더 자연스러워지며 공을 더 효과적으로 조절할 수 있게 됩니다.'])
                    problem.append('주 문제 ) 팔 굽힘 문제')
                elif(value==-1):
                    comment.append(['자세가 인식되지않습니다.','올바른 자세로 찍어주세요.',' '])  
                    problem.append(' ')
                 
            #뱌ㅐㄱ스윙
            elif(key=='backswing'): 
                
                if(value==1):
                    comment.append(['백스윙 구간에서 팔이 잘 펴졌어요',' ',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value<=155):
                    comment.append(['테이크어웨이 시 팔이 구부러져 있습니다.',
                                   '팔의 각도가 좁으면 스윙 동작이 제한되어 힘 전달이 어렵습니다.',
                                   '팔을 조금 더 펴준다면 스윙의 흐름이 더 자연스러워지며 공을 더 효과적으로 조절할 수 있게 됩니다.'])
                    problem.append('주 문제 ) 팔 굽힘 문제')
                elif(value==-1):
                    comment.append(['자세가 인식되지않습니다.','올바른 자세로 찍어주세요.',' '])    
                    problem.append(' ')
                   
            elif(key=='top'): #백스윙에서 팔 위치
                if(value==1):
                    comment.append(['볼을 끝까지 보는 시선 좋아요^^.',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value==0):
                    comment.append(['탑 구간에서 팔이 충분히 올라가지 못 하였습니다.',
                    '스윙 동작 중 팔을 조금 더 높게 들어올린다면 스윙의 일관성과 정확도를 향상시킬 수 있습니다.'])
                    problem.append('주 문제 ) 팔이 충분히 들어오지 않는 문제')
                elif(value==-1):
                    comment.append(['자세가 인식되지않습니다.','올바른 자세로 찍어주세요.'])    
                    problem.append(' ')
                    
            #임팩트
            #임팩트 시선
            elif(key=='impact_eye'):
                if(value==1):
                    comment.append(['임팩트 시 시선처리 좋아요!',' ',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value==0):
                    comment.append(['어드레스에서 임팩트 구간 동안 얼굴의 움직임을 최소화해야합니다.',
                    '또한 임팩트 시 얼굴이 공을 보고 있어야합니다.', 
                    '이런 정확한 시선은 공을 확실하게 타격하고 원하는 방향으로 보내는 데 도움이 됩니다.'
                    ])
                    problem.append('주 문제  ) 어드레스 - 임팩트 구간에서 얼굴 움직임 문제')
                elif(value==-1):
                    comment.append(['자세가 인식되지않습니다.','올바른 자세로 찍어주세요.',' '])   
                    problem.append(' ')
            
            #임펙트 무릎
            elif(key=='impact_knee'):
                if(value==1):
                    comment.append(['좋아요!',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value==0):
                    comment.append(['임팩트 과정에서 무릎의 간격이 넓습니다.', 
                    '두 무릎을 서로 가깝게 유지하여 특정한 동작이나 힘 전달을 높일 수 있습니다.'])
                    problem.append('주 문제 ) 무릎 간격 문제')
                elif(value==-1):
                    comment.append(['자세가 인식되지않습니다.','올바른 자세로 찍어주세요.']) 
                    problem.append('발의 너비')          
                    
            #임펙트 발거리
            elif(key=='impact_foot'):
                if(value==-1):
                    comment.append(['임팩트에서 피니시로 가는 과정에서 발의 간격이 넓습니다.',
                    '어드레스 구간에서의  발 간격을 최대한 유지해야 몸의 밸런스가 안정적이게 됩니다.'])
                    problem.append('주 문제 ) 발 간격 좁음 문제')
                elif(value==1):
                    comment.append(['어드레스의 발 사이의 거리가 좋아요^^.',' '])
                    total+=1
                    problem.append('S U C C E S S !')
                elif(value==0):
                    comment.append(['임팩트에서 피니시로 가는 과정에서 발의 간격이 조금 좁습니다.',
                    '어드레스 구간에서의  발 간격을 최대한 유지해야 몸의 밸런스가 안정적이게 됩니다.'])
                    problem.append('주 문제 )발 간격 넓음 문제')
        #넘기는 리스트 comment의 값은 총 7개
            # 어드레스 한개
            # 테이크어웨이 1개
            # 백스윙,백스윙탑 두개
            # 임팩트 3개
            
       
        
        # for i in range(7):
        #     for j in range(3):
        #         if comment[i][j]:
        #             print(comment[i][j])
        
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
        
        print(problem)
        
        #딕셔너리 값을 html로 넘김
        return render_template('index3.html',values=comment,xvalues=xtotal,tryn=tryn,file_name=file_name,total=total,problems=problem) 
        #problem은 주 문제
    else:
        return render_template('index2.html')
    
#마지막 페이지 점수,피드백 그리고 추가적으로 그래프
        
    

if __name__=='__main__':
    app.run(host="127.0.0.1",port="5000")