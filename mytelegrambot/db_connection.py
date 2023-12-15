import pymysql

connection = pymysql.connect(
    host='localhost',
    port='',
    user='username',
    password='db_password',
    db='db_name',
    cursorclass=pymysql.cursors.DictCursor
)
