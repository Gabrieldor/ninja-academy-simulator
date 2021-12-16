import requests
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

r = requests.get('https://docs.google.com/spreadsheets/d/1NIwQr0wtlKlOPl-TVMZpi0d2kxwodfbfIMJkKsxLfC0/edit#gid=0')
df = pd.read_html(r.content)[0]
df = df[['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S']]
df.columns = ['Action','Type','Technique','Action Cost','Aim','Damage','Status Self','Status Target','Hands','Icon','Id','MaxRNG','MinRNG','Node Name','Notes','Skill','Tier','Types','Description']
df.drop([0,1],inplace=True)
for i in df.index:
    row = df.loc[i]
    if type(row['Action']) == float:
        df.drop(i,inplace=True)
df.fillna('',inplace=True)


abilities = {}

for i in df.index:
    row = df.loc[i].str.lower()
    ability = {
        'aType':row['Type'],
        'technique':row['Technique'],
        'action':int(row['Action Cost']),
        'aim':int(row['Aim']),
        'dmg': split_dmg(row['Damage']),
        'status_self':row['Status Self'],
        'status_target':row['Status Target'],
        'hands':int(row['Hands']),
        'icon':f'resources/img/missing.png',
        'id':row['Id'],
        'maxRng':int(row['MaxRNG']),
        'minRng':int(row['MinRNG']),
        'name':row['Action'].capitalize(),
        'notes':row['Notes'],
        'skill':row['Skill'],
        'tier':int(row['Tier']),
        'types':get_types(row['Types']),
        'description':row['Description']
    }
    abilities[row['Technique'].lower()+"_"+row['Node Name'].replace('-','_')] = ability
with open('unarmed_abilities.json','w',encoding='utf-8') as f:
        jresult = json.dumps(abilities,indent=2 ,sort_keys=True,ensure_ascii=False)
        f.write(jresult)

