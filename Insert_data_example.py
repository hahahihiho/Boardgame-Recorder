import pandas as pd
import _2_DB as db

if __name__ == "__main__":
    path = './모임내역-2020년.xlsx'
    df = pd.read_excel(path,sheet_name=None,header=1)
    date_list = df['1월']['모임일자']
    other_list = df['1월']['돌아간게임']

    ## data -> insert
    # 데이터형식
    # {'data': [{'date': '2020-01-03',
    #    'seq': 0,
    #    'gamename': '이스탄불 : 빅박스',
    #    'name_list': ['Gom', ' 털업', ' 라곰이']},
    data = {'data':[]}
    counter = 0
    for date,dayRows in zip(date_list,other_list):

        dayRow_list = dayRows.split('\n')
        last_L_bracket_i = map(lambda x: x.rfind('('),dayRow_list)
        last_R_bracket_i = map(lambda x: x.rfind(')'),dayRow_list)
        
        for j,(row,L,R) in enumerate(zip(dayRow_list,last_L_bracket_i,last_R_bracket_i)):
            data['data'].append({})
            data['data'][counter]['date'] = date.strftime('%Y-%m-%d')
            data['data'][counter]['seq'] = j
            data['data'][counter]['gamename'] = row[0:L].strip()
            data['data'][counter]['name_list'] = row[L+1:R].split(',')
            counter += 1
    
    db.createTable()
    for _ in data['data']:
        db.insertData(_)