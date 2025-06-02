import pymysql

# mysql> desc test;
# +-------+---------------+------+-----+---------+----------------+
# | Field | Type          | Null | Key | Default | Extra          |
# +-------+---------------+------+-----+---------+----------------+
# | id    | int           | NO   | PRI | NULL    | auto_increment |
# | name  | varchar(50)   | NO   |     | NULL    |                |
# | sex   | enum('f','m') | NO   |     | m       |                |
# | age   | int unsigned  | NO   |     | NULL    |                |
# +-------+---------------+------+-----+---------+----------------+
# 4 rows in set (0.01 sec)

try:
    connect_mysql = pymysql.connect(
        host='192.168.74.134',
        port=3306,
        user='python_mysql',
        password='python_mysql',
        database='python_mysql'
    )

    with connect_mysql.cursor() as cursor:
        sql = 'select * from test'
        cursor.execute(sql)
        print('before insert')
        for row in cursor.fetchall():
            print(row)
        cursor.execute('insert into test(name, sex, age) values ("bob", "f", 20)')
        connect_mysql.commit()
        cursor.execute('select * from test')
        print('after insert')
        for row in cursor.fetchall():
            print(row)
        cursor.execute('delete from test where id>2')
        connect_mysql.commit()
        cursor.execute('select * from test')
        print('after delete')
        for data in cursor.fetchall():
            print(data)



except Exception as e:
    print(e)