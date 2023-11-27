import pymysql

db=pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='1234',
    db='golf',
    charset='utf8')
cursor=db.cursor()