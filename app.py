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
#
# *** study more ***
# ERD 바탕으로 db 모델링 최적화..
########################


from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
import sqlite3
import os
import _2_DB as db
import pandas as pd

app=Flask(__name__)
db_path = './db/boardgame.sql'
if not os.path.exists(db_path):
    db.createTable()

# app
# record page
@app.route('/',methods=['GET'])
def main():
    table = []
    return render_template('index.html',table=table)


@app.route('/date',methods=['POST'])
def get_date():
    req = request.get_json()
    day_list=['일','월','화','수','목','금','토']
    table = db.showDateTable(req)
    day = day_list[req['day']]
    output = {'table':table, 'day': day}

    res = make_response(jsonify(output), 200)
    print(req)
    print(table)
    print(type(res),res)
    return res

@app.route('/addRecord',methods=['POST'])
def get_data():
    req = request.get_json()
    print('addRecord req : \n',req)
    req['name_list'] = req['name_list'].split(',')
    db.insertData(req)
    output = db.showDateTable(req)
    res = make_response(jsonify(output),200)
    return res

@app.route('/delRecord',methods=['POST'])
def del_Record():
    req = request.get_json()
    print('delRecord req: \n',req)
    db.delRecord_correctSeq(req)
    output = db.showDateTable(req)
    res = make_response(jsonify(output),200)
    return res

@app.route('/swapRecord',methods=['POST'])
def swap_Record():
    req = request.get_json()
    print('swap_Record req: \n',req)
    db.swapRecordSeq(req)
    output = db.showDateTable(req)
    res = make_response(jsonify(output),200)
    return res

# @app.route('/showall', methods=['GET','POST'])
# def showall():
#     if request.method == 'GET':
#         createTable()
#         table = selectAllSQL()
#         return render_template('record_view.html',table=table)

#     elif request.method=='POST':
#         # 고객정보 수정,삭제
#         req = request.form
#         idx = req.get('idx')
#         date = req.get('date')
#         boardgame = req.get('boardgame')
#         nickname = req.get('players')
#         action = request.form.get('action')
#         if action == 'update':
#             data = [date,boardgame,nickname,idx]
#             updateSQL(data)
#         else :
#             deleteSQL(idx)

#         return redirect('/showall')

# 통계 페이지
@app.route('/statistic')
def statistics():
    return render_template('statistic_main.html')

@app.route('/chartOverall',methods=['GET'])
def chart_overall():
    print('chart_overall()')
    output = {'chart_game_play':db.chart_game_play()}
    output['chart_member_attend']=db.chart_member_attend()
    output['chart_member_play']=db.chart_member_play()
    # print(output)
    res = make_response(jsonify(output),200)
    return res

# statistic_boardgame
@app.route('/statisticBoardgame')
def statistics_Boardgames():
    output = db.selectAllBoardgame()
    game_list = output['name']
    year_list = db.selectAllYear()
    year_list = year_list['year']
    return render_template('statistic_boardgame.html',game_list=game_list,year_list=year_list)

@app.route('/chart_boardgame',methods=['GET'])
def chart_boardgame():
    print('chart_boardgame()')
    output = {'chart_game_play':db.chart_game_play()}
    output['chart_member_attend']=db.chart_member_attend()
    output['chart_member_play']=db.chart_member_play()
    print(output)
    res = make_response(jsonify(output),200)
    return res

@app.route('/statistic/dataset/game_year',methods=['POST'])
def checked_game_list():
    req = request.get_json()
    print('checked_game_list\n',req)
    output = db.chart_game_everymonth_fixedyear(req)
    output['game_name'] = req['game_name']
    print(output)
    res = make_response(jsonify(output),200)
    return res

### statistic member

@app.route('/statisticMember')
def statistics_Members():
    output = db.selectAllMember()
    member_list = output['name']
    year_list = db.selectAllYear()
    year_list = year_list['year']
    return render_template('statistic_member.html',member_list=member_list,year_list=year_list)

    

@app.route('/statistic/dataset/member_year',methods=['POST'])
def checked_member_list():
    req = request.get_json()
    print('checked_member_list\n',req)
    output = db.chart_member_everymonth_fixedyear(req)
    output['member_name'] = req['member_name']
    print(output)
    res = make_response(jsonify(output),200)
    return res





# host='0.0.0.0' => 내 ip접속 허용
if __name__=='__main__':
    app.run(host = '0.0.0.0',debug=True)