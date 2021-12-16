import pandas as pd
import json

def split_dmg(dmg):
    result = {}
    f_split = dmg.split('d')
    result['num'] = int(f_split[0])
    s_split = f_split[1].split('+')
    try:
        result['d'] = int(s_split[0])
        result['add'] = int(s_split[1])
    except:
        s_split = f_split[1].split('-')
        result['d'] = int(s_split[0])
        result['add'] = int(s_split[1])
    return result
def get_types(types):
    result = {}
    type = types.split(',')
    for t in type:
        t = t.replace(' ','')
        result[t] = True
    return result

df = pd.read_csv('Database Spreadsheets - Melee Weapons.csv')
df.drop([0,1],inplace=True)
for i in df.index:
    row = df.loc[i]
    if type(row['Action']) == float:
        df.drop(i,inplace=True)
df.fillna('',inplace=True)

abilities = {}

for i in df.index:
    row = df.loc[i]
    ability = {
        'aType':row['Type'].lower(),
        'technique':row['Technique'].lower(),
        'action':int(row['Action Cost']),
        'aim':int(row['Aim']),
        'dmg': split_dmg(row['Damage']),
        'status_self':row['Status Self'],
        'status_target':row['Status Target'].lower(),
        'hands':int(row['Hands']),
        'icon':f'resources/img/missing.png',
        'id':row['Id'].lower(),
        'maxRng':int(row['MaxRNG']),
        'minRng':int(row['MinRNG']),
        'name':row['Action'],
        'notes':row['Notes'],
        'skill':row['Skill'],
        'tier':int(row['Tier']),
        'types':get_types(row['Types']),
        'description':row['Description']
    }
    abilities[row['Technique'].lower()+"_"+row['Node Name'].replace('-','_')] = ability
with open('melee_weapons.json','w',encoding='utf-8') as f:
        jresult = json.dumps(abilities,indent=2 ,sort_keys=True,ensure_ascii=False)
        f.write(jresult)

