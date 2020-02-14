########################
# 제작: 2020/01/20
# 수정: 
# 제작자: 조현명(https://github.com/hahahihiho)
# title: 보드게임 기록
########################
# ***Brief Description***
# readme.md 로 대체
#
# *** study more ***
# Mongo.DB 사용..
########################


from flask import Flask, render_template, request, url_for, redirect, jsonify, make_response
import sqlite3
import os
import _2_DB as db
import pandas as pd
import numpy as np

app=Flask(__name__)
db_path = './db/boardgame.sql'
if not os.path.exists(db_path):
    db.createTable()

### record page
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


### statistic main
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

### statistic_boardgame
@app.route('/statisticBoardgame')
def statistics_Boardgames():
    output = db.selectAllBoardgame()
    game_list = output['name']
    year_list = db.selectAllYear()
    year_list = year_list['year']
    return render_template('statistic_boardgame.html',game_list=game_list,year_list=year_list)

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

### manage
@app.route('/manage')
def manage_page():
    member_play = db.selectMemberPlay()
    a = np.array(member_play['name'])
    b = np.array(member_play['N_of_play'])
    c = np.concatenate((a,b),axis=0)
    member_table = np.reshape(c,(-1,2),order='F')
    print(member_table)
    game_play = db.selectGamePlay()
    a = np.array(game_play['name'])
    b = np.array(game_play['N_of_play'])
    c = np.concatenate((a,b),axis=0)
    game_table = np.reshape(c,(-1,2),order='F')
    return render_template('manager_page.html',member_table = member_table,game_table = game_table)

### autocomplete_list
@app.route('/members')
def member_list():
    output = db.selectAllMember()
    res = make_response(jsonify(output['name']),200)
    return res

@app.route('/boardgames')
def game_list():
    output = db.selectAllBoardgame()
    res = make_response(jsonify(output['name']),200)
    return res

### periodic
@app.route('/statistic/periodic/boardgame')
def statistic_periodic_boardgame():
    return render_template('periodic_boardgame.html')

@app.route('/statistic/periodic/member')
def statistic_periodic_member():
    return render_template('periodic_member.html')
#### form
@app.route('/periodic/member',methods=['POST'])
def get_start_end_date_from_member():
    req = request.get_json()
    print(req)
    start_date = req['start_date']
    end_date = req['end_date']
    if start_date=='' or end_date=='':
        return 'empty'
    elif end_date<start_date:
        return 'correct date order'
    # correct
    else:
        output = db.members_attendtime_from_certain_period(req)
        print(output)
        res = make_response(jsonify(output), 200)
        return res

@app.route('/periodic/boardgame',methods=['POST'])
def get_start_end_date_from_boardgame():
    req = request.get_json()
    start_date = req['start_date']
    end_date = req['end_date']
    if start_date=='' or end_date=='':
        return 'empty'
    elif end_date<start_date:
        return 'correct date order'
    # correct
    else:
        output = db.boardgames_playtime_from_certain_period(req)
        print(output)
        res = make_response(jsonify(output), 200)
        return res



# host='0.0.0.0' => 내 ip접속 허용
if __name__=='__main__':
    app.run(host = '0.0.0.0',debug=True)