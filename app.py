########################
# 제작: 2020/01/20
# 수정: 
# 제작자: 조현명(https://github.com/hahahihiho)
# title: 보드게임 기록
########################
# ***Brief Description***
# 보드게임 record를 flask로 web에 구현
# insert,update,delete,date-search,show-statistics 기능 구현
# virtualenv or venv 와 gunicorn을 이용하여 heruko에 배포
########################


from flask import Flask,render_template,request,url_for,redirect
import sqlite3
import pandas as pd

app=Flask(__name__)
db_path = './db/boardgame.sql'
table_name = 'BDRecorder'
# data_tuple = ('date','boardgame','nickname')

## this is for general sql_excuter(Future version)
# def execute_sql(sql:str,keys:iter):
#     print(sql,keys)
#     data=c.execute(sql,keys)
#     # select
#     data=c.fetchall()
#     return data

def createTable():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='''    
        create table if not exists {}(
            idx INTEGER PRIMARY KEY AUTOINCREMENT,
            date text,
            boardgame text,
            nickname text
        )
    '''.format(table_name)
    cur.execute(sql)

    conn.commit()
    conn.close()

def insertSQL(data):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='insert into {}(date,boardgame,nickname) values(?,?,?)'.format(table_name)
    cur.execute(sql,data)

    conn.commit()
    conn.close()

def selectAllSQL():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='select * from {}'.format(table_name)
    cur.execute(sql)

    customerList = cur.fetchall()

    conn.commit()
    conn.close()
    return customerList

def updateSQL(data):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='UPDATE {} SET date=?,boardgame=?,nickname=? WHERE idx=?'.format(table_name)
    print(sql)
    cur.execute(sql,data)

    conn.commit()
    conn.close()


def deleteSQL(idx):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='DELETE FROM {} WHERE idx=?'.format(table_name)
    cur.execute(sql,(idx,))

    conn.commit()
    conn.close()

def selectSQL(date):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='select * from {} where date=?'.format(table_name)
    cur.execute(sql,(date,))
    data = cur.fetchall()
    conn.commit()
    conn.close()

    return data

# app
@app.route('/',methods=['GET','POST'])
def main():
    if request.method=='GET':
        return render_template('index.html')
    else:
        # 기록
        date = request.form.get('date')
        boardgame_list = request.form.getlist('boardgame')
        players_list = request.form.getlist('players')
        for boardgame,players in zip(boardgame_list,players_list):
            player_list = players.split(',')
            for nickname in player_list:
                insertSQL([date,boardgame,nickname])
        return redirect('/')

@app.route('/showall', methods=['GET','POST'])
def showall():
    if request.method == 'GET':
        createTable()
        table = selectAllSQL()
        return render_template('record_view.html',table=table)

    elif request.method=='POST':
        # 고객정보 수정,삭제
        req = request.form
        idx = req.get('idx')
        date = req.get('date')
        boardgame = req.get('boardgame')
        nickname = req.get('players')
        action = request.form.get('action')
        if action == 'update':
            data = [date,boardgame,nickname,idx]
            updateSQL(data)
        else :
            deleteSQL(idx)

        return redirect('/showall')

@app.route('/statistic')
def statistics():
    data=selectAllSQL()
    df = pd.DataFrame(data,columns=['idx','date','boardgame','nickname'])
    print(df)

    b_count=df.boardgame.value_counts()
    n_count=df.nickname.value_counts()
    print(b_count,n_count)
    b_dic={}
    n_dic={}
    for i,v in zip(b_count.index,b_count):
        b_dic[i]=v
    for i,v in zip(n_count.index,n_count):
        n_dic[i]=v
    return render_template('statistic.html',boardgame=b_dic,nickname=n_dic)


# host='0.0.0.0' => 내 ip접속 허용
if __name__=='__main__':
    app.run(debug=True)