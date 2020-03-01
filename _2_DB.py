import sqlite3
import numpy as np

db_path = './db/boardgame.sql'
# BMM = 'BOARDGAME_MEMBER_MAPPER'
# RMM = 'RECORD_MEMBER_MAPPER'
# TR = 'RECORD'
# TB = 'BOARDGAME'
# TM = 'MEMBER'
# id_r = 'record_id'
# id_b = 'game_id'
# id_m = 'member_id'

def createTable():
    conn=sqlite3.connect(db_path)
    conn.execute('pragma foreign_keys=ON')
    cur=conn.cursor()
    # RECORD
    sql = '''
    CREATE TABLE IF NOT EXISTS RECORD (
        record_id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        seq INTEGER NOT NULL
    )'''
    cur.execute(sql)

    # BOARDGAME
    sql = '''
    CREATE TABLE IF NOT EXISTS BOARDGAME (
        game_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )'''
    cur.execute(sql)

    # MEMBER
    sql = '''
    CREATE TABLE IF NOT EXISTS MEMBER (
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )'''
    cur.execute(sql)

    # RECORD_BOARDGAME_MAPPER
    sql = '''
    CREATE TABLE IF NOT EXISTS {table1}_{table2}_MAPPER (
        {id1} INTEGER,
        {id2} INTEGER,
        PRIMARY KEY({id1},{id2})
        CONSTRAINT fk_{table1}_{table2}_{id1}
            FOREIGN KEY ({id1}) REFERENCES {table1} ({id1})
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_{table1}_{table2}_{id2}
            FOREIGN KEY ({id2}) REFERENCES {table2} ({id2})
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )'''.format(table1='RECORD',table2='BOARDGAME',id1 = 'record_id' ,id2 = 'game_id')

    cur.execute(sql)

    # RECORD_MEMBER_MAPPER
    sql = '''
    CREATE TABLE IF NOT EXISTS {table1}_{table2}_MAPPER (
        {id1} INTEGER,
        {id2} INTEGER,
        PRIMARY KEY({id1},{id2})
        CONSTRAINT fk_{table1}_{table2}_{id1}
            FOREIGN KEY ({id1}) REFERENCES {table1} ({id1})
            ON DELETE CASCADE
            ON UPDATE CASCADE,
        CONSTRAINT fk_{table1}_{table2}_{id2}
            FOREIGN KEY ({id2}) REFERENCES {table2} ({id2})
            ON DELETE CASCADE
            ON UPDATE CASCADE
    )'''.format(table1='RECORD',table2='MEMBER',id1 = 'record_id' ,id2 = 'member_id')

    cur.execute(sql)

# I made it for study, but it is not useful and problem when deleting the record
    # BOARDGAME_MEMBER_MAPPER
    # sql = '''
    # CREATE TABLE IF NOT EXISTS {table1}_{table2}_MAPPER (
    #     {id1} INTEGER,
    #     {id2} INTEGER,
    #     CONSTRAINT fk_{table1}_{table2}_{id1}
    #         FOREIGN KEY ({id1}) REFERENCES {table1} ({id1})
    #         ON DELETE CASCADE
    #         ON UPDATE CASCADE,
    #     CONSTRAINT fk_{table1}_{table2}_{id2}
    #         FOREIGN KEY ({id2}) REFERENCES {table2} ({id2})
    #         ON DELETE CASCADE
    #         ON UPDATE CASCADE
    # )'''.format(table1='BOARDGAME',table2='MEMBER',id1 = 'game_id' ,id2 = 'member_id')
    # cur.execute(sql)

    conn.commit()
    conn.close()

# sql connect decorator(Rjson,Return,no return)
def connectSqlRjson(f):
    def function(*args, **kwargs):
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        conn.execute('pragma foreign_keys=ON')

        sql = f(*args, **kwargs)
        sql_list = sql.split(';')
        for query in sql_list:
            # try:
            # print(query)
            cur.execute(query)
            # except:
            #     raise ValueError(query)
        result = {'keys':[],'values':[]}
        result['columns']=[_[0] for _ in cur.description]
        query_result = cur.fetchall()
        for _ in query_result:
            result['keys'].append(_[0])
            result['values'].append(_[1])
        conn.commit()
        conn.close()
        return result
    return function

# return
def connectSqlr(f):
    def function(*args, **kwargs):
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        conn.execute('pragma foreign_keys=ON')

        sql = f(*args, **kwargs)
        sql_list = sql.split(';')
        for query in sql_list:
            # try:
            print(query)
            cur.execute(query)
            # except:
            #     raise ValueError(query)
        result = {}
        result['columns']=[_[0] for _ in cur.description]
        query_result = cur.fetchall()
        query_result = np.array(query_result).T
        print(result['columns'],query_result)
        print(query_result.shape)
        if query_result.shape[0] == len(result['columns']):
            for i,_ in enumerate(result['columns']):
                result[_] = list(query_result[i])
        else :
            for i,_ in enumerate(result['columns']):
                result[_] = []
        print(result)
        conn.commit()
        conn.close()
        return result
    return function

def connectSqlRmonth(f):
    def function(*args, **kwargs):
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        conn.execute('pragma foreign_keys=ON')

        sql = f(*args, **kwargs)
        sql_list = sql.split(';')
        for query in sql_list:
            # try:
            # print(query)
            cur.execute(query)
            # except:
            #     raise ValueError(query)
        result = {}
        result['columns']=[_[0] for _ in cur.description]
        query_result = cur.fetchall()
        
        ## None 값을 가지고 있을 시 0으로 초기화
        if query_result[0][0]==None:
            result['value']=[0]*12
        ## tuple to list [()] -> []
        else:        
            result['value'] = list(query_result[0])
        # print(result)

        conn.commit()
        conn.close()
        return result
    return function

# No Return
def connectSql(f):
    def function(*args, **kwargs):
        conn=sqlite3.connect(db_path)
        cur=conn.cursor()
        conn.execute('pragma foreign_keys=ON')

        sql = f(*args, **kwargs)
        sql_list = sql.split(';')
        for query in sql_list:
            # try:
            print(query)
            cur.execute(query)
            # except:
            #     raise ValueError(query)

        conn.commit()
        conn.close()
    return function

### end decorator

# insert row
def insertData(data):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    conn.execute('pragma foreign_keys=ON')

    sql= '''
    INSERT INTO RECORD (date,seq)
        SELECT '{date}',{seq}
        WHERE NOT EXISTS (
            SELECT 1 FROM RECORD WHERE date = '{date}' AND seq = {seq}
        );
    INSERT INTO BOARDGAME (name)
        SELECT '{gamename}'
        WHERE NOT EXISTS (
            SELECT 1 FROM BOARDGAME WHERE name = '{gamename}'
        );
    INSERT OR IGNORE INTO RECORD_BOARDGAME_MAPPER (record_id,game_id)
        SELECT RECORD.record_id,BOARDGAME.game_id
            FROM RECORD,BOARDGAME
            WHERE RECORD.date = '{date}' AND RECORD.seq = {seq}
                AND BOARDGAME.name = '{gamename}';
    '''.format(date=data['date'], seq=data['seq'], gamename=data['gamename'])
        
    sql_list = sql.split(';')
    for query in sql_list:
        cur.execute(query)

    for name in data["name_list"]:
        sql = '''
        INSERT INTO MEMBER (name)
            SELECT '{name}'
            WHERE NOT EXISTS (
                SELECT 1 FROM MEMBER WHERE name = '{name}'
            );
        INSERT OR IGNORE INTO RECORD_MEMBER_MAPPER (record_id,member_id)
            SELECT RECORD.record_id,MEMBER.member_id
            FROM RECORD,MEMBER
            WHERE RECORD.date = '{date}' AND RECORD.seq = {seq}
                AND MEMBER.name = '{name}'
        '''.format(date=data['date'], seq=data['seq'], name=name.strip())

        sql_list = sql.split(';')
        for query in sql_list:
            cur.execute(query)
    conn.commit()
    conn.close()

def showDateTable(data):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    conn.execute('pragma foreign_keys=ON')

    sql = '''
    select R.*,B.name, GROUP_CONCAT(M.name) AS players from RECORD AS R
        LEFT JOIN RECORD_BOARDGAME_MAPPER RBM
            ON R.record_id = RBM.record_id
        LEFT JOIN BOARDGAME B
            ON RBM.game_id = B.game_id
        LEFT JOIN RECORD_MEMBER_MAPPER RMM
            ON R.record_id = RMM.record_id
        LEFT JOIN MEMBER M
            ON RMM.member_id = M.member_id
    WHERE R.date = '{date}'
    GROUP BY R.record_id
    ORDER BY R.seq ASC
    '''.format(date = data['date'])
    
    cur.execute(sql)
    header = [_[0] for _ in cur.description]
    sqlist = cur.fetchall()
    conn.commit()
    conn.close()
    print(header)

    json = []
    for _ in sqlist:
        # print(_)
        temp_dic = {}
        temp_dic['seq'] = _[2]
        temp_dic['gamename'] = _[3]
        temp_dic['name_list'] = _[4]
        json.append(temp_dic)

    return json

### select ###
@connectSqlr
def selectAllBoardgame():
    sql = 'select name from BOARDGAME ORDER BY name ASC'
    return sql

@connectSqlr
def selectAllMember():
    sql = 'select name from MEMBER ORDER BY name ASC'
    return sql

@connectSqlr
def selectAllYear():
    sql = 'select strftime("%Y",date) AS year from RECORD GROUP BY year ORDER BY year ASC'
    return sql
### end select ###
### manage page
@connectSqlr
def selectMemberPlay():
    sql = '''
    SELECT M.name,COUNT(RMM.record_id) AS N_of_play FROM MEMBER AS M
        LEFT JOIN RECORD_MEMBER_MAPPER AS RMM
        ON M.member_id = RMM.member_id
    GROUP BY M.name
    ORDER BY N_of_play DESC,M.name ASC
    '''
    return sql

@connectSqlr
def selectGamePlay():
    sql = '''
    SELECT B.name,COUNT(RBM.record_id) AS N_of_play FROM BOARDGAME AS B
        LEFT JOIN RECORD_BOARDGAME_MAPPER AS RBM
        ON B.game_id = RBM.game_id
    GROUP BY B.name
    ORDER BY B.name ASC
    '''
    return sql

### end

### delete member, game ###
@connectSql
def deleteBoardgame(data):
    sql = '''
    DELETE FROM BOARDGAME WHERE name = '{name}'
    '''.format(name = data['game_name'])
    return sql

@connectSql
def deleteMember(data):
    sql = '''
    DELETE FROM MEMBER WHERE name = '{name}'
    '''.format(name = data['name'])
    return sql
### end ###

# 합쳐서 구현.. 나눠서 보기좋게 효율적으로 구현할 방법은..
# @connectSql
# def deleteRecord(data):
#     sql = '''
#     DELETE FROM RECORD
#     WHERE date = '{date}' AND seq = {seq}
#     '''.format(date=data['date'],seq=data['seq'])
#     correctSeq(data)
#     return sql

# @connectSql
# def correctSeq(data):
#     sql = '''
#     UPDATE RECORD
#     SET seq = seq -1
#     WHERE date = '{date}' AND seq > {seq}
#     '''.format(date = data['date'],seq = data['seq'])
#     return sql

### manage record table ###
@connectSql
def delRecord_correctSeq(data):
    sql = '''
    DELETE FROM RECORD
    WHERE date = '{date}' AND seq = {seq};
    UPDATE RECORD
    SET seq = seq -1
    WHERE date = '{date}' AND seq > {seq}
    '''.format(date=data['date'],seq=data['seq'])
    return sql

@connectSql
def swapRecordSeq(data):
    # sql = '''
    # UPDATE RECORD AS R
    # SET seq = (CASE WHEN seq = {seq1} then {seq2} else {seq1} end)
    # WHERE date = '{date}' AND seq IN ({seq1},{seq2})
    # '''.format(date = data['date'],seq1 = data['seq1'],seq2 = data['seq2'])
    sql = '''
    UPDATE RECORD
    SET seq = CASE seq
        WHEN {seq1} THEN {seq2}
        WHEN {seq2} THEN {seq1}
    END
    WHERE date = '{date}' AND seq IN ({seq1},{seq2})
    '''.format(date = data['date'],seq1 = data['seq1'],seq2 = data['seq2'])
    return sql
### end ###

### /statistic ChartData ###
@connectSqlRjson
def chart_game_play():
    sql = '''
    SELECT B.name,COUNT(RBM.game_id) AS game_freq FROM RECORD_BOARDGAME_MAPPER AS RBM
        LEFT JOIN BOARDGAME AS B ON RBM.game_id = B.game_id  
    GROUP BY RBM.game_id
    ORDER BY game_freq DESC
    '''
    return sql

@connectSqlRjson
def chart_member_attend():
    sql = '''
    SELECT M.name,COUNT(M.member_id) AS MEM_ATT FROM (
        SELECT * FROM RECORD AS R
            LEFT JOIN RECORD_MEMBER_MAPPER AS RMM
            ON R.record_id = RMM.record_id
        GROUP BY R.date,RMM.member_id
    ) AS subT
    LEFT JOIN MEMBER AS M
    ON subT.member_id = M.member_id
    GROUP BY M.member_id
    ORDER BY MEM_ATT DESC,M.name ASC
    '''
    return sql

@connectSqlRjson
def chart_member_play():
    sql = '''
    SELECT M.name,COUNT(RMM.member_id) AS mem_play FROM RECORD_MEMBER_MAPPER AS RMM
        LEFT JOIN MEMBER AS M ON RMM.member_id = M.member_id  
    GROUP BY RMM.member_id
    ORDER BY mem_play DESC
    '''
    return sql
### END ###

# def list_to_tuple_str(l):
#     return '("'+'","'.join(l)+'")'

### /statistic_boardgame Chart ###
@connectSqlRmonth
def chart_game_everymonth_fixedyear(data):
    sql = '''
    SELECT 
        SUM(CASE strftime('%m',R.date) WHEN '01' THEN 1 ELSE 0 END) AS January,
        SUM(CASE WHEN strftime('%m',R.date) = '02' THEN 1 ELSE 0 END) AS Februrary,
        SUM(CASE WHEN strftime('%m',R.date) = '03' THEN 1 ELSE 0 END) AS March,
        SUM(CASE WHEN strftime('%m',R.date) = '04' THEN 1 ELSE 0 END) AS April,
        SUM(CASE WHEN strftime('%m',R.date) = '05' THEN 1 ELSE 0 END) AS May,
        SUM(CASE WHEN strftime('%m',R.date) = '06' THEN 1 ELSE 0 END) AS June,
        SUM(CASE WHEN strftime('%m',R.date) = '07' THEN 1 ELSE 0 END) AS July,
        SUM(CASE WHEN strftime('%m',R.date) = '08' THEN 1 ELSE 0 END) AS August,
        SUM(CASE WHEN strftime('%m',R.date) = '09' THEN 1 ELSE 0 END) AS September,
        SUM(CASE WHEN strftime('%m',R.date) = '10' THEN 1 ELSE 0 END) AS October,
        SUM(CASE WHEN strftime('%m',R.date) = '11' THEN 1 ELSE 0 END) AS November,
        SUM(CASE WHEN strftime('%m',R.date) = '12' THEN 1 ELSE 0 END) AS December
    FROM RECORD AS R
        LEFT JOIN RECORD_BOARDGAME_MAPPER AS RBM
        ON R.record_id = RBM.record_id
        LEFT JOIN BOARDGAME AS B
        ON RBM.game_id = B.game_id
    WHERE B.name = '{game_name}' AND strftime('%Y',R.date) = '{year}'
    '''.format(game_name = data['game_name'],year = data['year'])
    return sql

@connectSqlRmonth
def chart_member_everymonth_fixedyear(data):
    sql = '''
    SELECT 
        SUM(CASE strftime('%m',R.date) WHEN '01' THEN 1 ELSE 0 END) AS January,
        SUM(CASE WHEN strftime('%m',R.date) = '02' THEN 1 ELSE 0 END) AS Februrary,
        SUM(CASE WHEN strftime('%m',R.date) = '03' THEN 1 ELSE 0 END) AS March,
        SUM(CASE WHEN strftime('%m',R.date) = '04' THEN 1 ELSE 0 END) AS April,
        SUM(CASE WHEN strftime('%m',R.date) = '05' THEN 1 ELSE 0 END) AS May,
        SUM(CASE WHEN strftime('%m',R.date) = '06' THEN 1 ELSE 0 END) AS June,
        SUM(CASE WHEN strftime('%m',R.date) = '07' THEN 1 ELSE 0 END) AS July,
        SUM(CASE WHEN strftime('%m',R.date) = '08' THEN 1 ELSE 0 END) AS August,
        SUM(CASE WHEN strftime('%m',R.date) = '09' THEN 1 ELSE 0 END) AS September,
        SUM(CASE WHEN strftime('%m',R.date) = '10' THEN 1 ELSE 0 END) AS October,
        SUM(CASE WHEN strftime('%m',R.date) = '11' THEN 1 ELSE 0 END) AS November,
        SUM(CASE WHEN strftime('%m',R.date) = '12' THEN 1 ELSE 0 END) AS December
    FROM RECORD AS R
        LEFT JOIN RECORD_MEMBER_MAPPER AS RMM
        ON R.record_id = RMM.record_id
        LEFT JOIN MEMBER AS M
        ON RMM.member_id = M.member_id
    WHERE M.name = '{member_name}' AND strftime('%Y',R.date) = '{year}'
    '''.format(member_name = data['member_name'],year = data['year'])
    return sql

### END ###

### periodic
@connectSqlRjson
def members_attendtime_from_certain_period(data):
    sql = '''
    SELECT M.name,COUNT(M.member_id) AS MEM_ATT FROM (
        SELECT * FROM RECORD AS R
            LEFT JOIN RECORD_MEMBER_MAPPER AS RMM ON R.record_id = RMM.record_id
        GROUP BY R.date,RMM.member_id
    ) AS subT
    LEFT JOIN MEMBER AS M ON subT.member_id = M.member_id
    WHERE subT.date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY M.member_id
    ORDER BY MEM_ATT DESC
    '''.format(start_date=data['start_date'],end_date=data['end_date'])
    return sql

@connectSqlRjson
def boardgames_playtime_from_certain_period(data):
    sql = '''
    SELECT B.name,COUNT(RBM.game_id) AS game_freq FROM RECORD AS R
        LEFT JOIN RECORD_BOARDGAME_MAPPER AS RBM ON R.record_id = RBM.record_id
        LEFT JOIN BOARDGAME AS B ON RBM.game_id = B.game_id  
    WHERE R.date BETWEEN '{start_date}' AND '{end_date}'
    GROUP BY RBM.game_id
    ORDER BY game_freq DESC
    '''.format(start_date=data['start_date'],end_date=data['end_date'])
    return sql



#################################
########### FOR TEST ############
#################################
@connectSqlr
def selectFromRecord(data):
    sql='''
    select * from RECORD WHERE date = {date}
    '''.format(date=data['date'])
    return sql

def selectTable(table_name):
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()
    sql='select * from {}'.format(table_name)
    cur.execute(sql)

    customerList = cur.fetchall()
    print(customerList)
    conn.commit()
    conn.close()

def showJoinTable():
    conn=sqlite3.connect(db_path)
    cur=conn.cursor()

    sql = '''
    select R.*,B.name AS game,M.name from RECORD R
        LEFT JOIN RECORD_BOARDGAME_MAPPER RBM
            ON R.record_id = RBM.record_id
        LEFT JOIN BOARDGAME B
            ON RBM.game_id = B.game_id
        LEFT JOIN RECORD_MEMBER_MAPPER RMM
            ON R.record_id = RMM.record_id
        LEFT JOIN MEMBER M
            ON RMM.member_id = M.member_id
    '''
    cur.execute(sql)
    table = cur.fetchall()
    print([_[0] for _ in cur.description])
    for _ in table:
        print(_)    

    conn.commit()
    conn.close()
    return table
