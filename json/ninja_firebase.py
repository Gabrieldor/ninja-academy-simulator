import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import gspread
from google.oauth2 import service_account
from firebase_admin import db
import pandas as pd
import json

def connect_spreadsheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
    json_file = "ninja_cred.json"
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc

def path_to_img(name):
    bucket = storage.bucket()
    blob = bucket.get_blob(f'abilities_icons/{name}.png')
    if blob is not None:
        path = 'https://firebasestorage.googleapis.com/v0' + blob.path + '?alt=media&token=' + blob.metadata['firebaseStorageDownloadTokens']
        return path
    else:
        return 'resources/img/missing.png'

def get_csvs():
    dfs = []
    gc = connect_spreadsheet()
    spreadsheet = gc.open("Database Spreadsheets")
    sheet_names = spreadsheet.worksheets()
    for name in sheet_names:
        if name.title != "Ways":
            sheet = spreadsheet.worksheet(name.title)
            dados = sheet.get_all_records()
            df = pd.DataFrame(dados)
            dfs.append(df)
    
    return dfs

def get_some_csvs(*names):
    dfs = []
    gc = connect_spreadsheet()
    spreadsheet = gc.open("Database Spreadsheets")
    for name in names:
        sheet = spreadsheet.worksheet(name)
        dados = sheet.get_all_records()
        df = pd.DataFrame(dados)
        dfs.append(df)
    
    return dfs

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

def retrieve_status(statuses,status_keys_list,conditions):
    global status_name
    for status in statuses:
        status_split = status.split(' ')
        for piece in status_split:
            if piece in status_keys_list:
                status_name = piece
            elif piece.isdigit():
                status_x = piece
            elif piece in status_keys_list:
                status_extra = piece
        status_db = db.reference(f'proto/conditions/{status_name}').get()
        try:
            if status_db == None:
                raise Exception
            try:
                currentAdd = status_db['currentAdd']
                for i in currentAdd:
                    try:
                        num = currentAdd[i]
                        if num < 0:
                            currentAdd[i] = -status_x
                        else:
                            currentAdd[i] = status_x
                    except:
                        pass
                conditions[status_name] = currentAdd
            except:
                pass

            try:
                maxAdd = status_db['maxAdd']
                conditions[status_name] = maxAdd
            except:
                pass

        except:
            conditions[status] = "Not implemented yet!"

        status_name = None


def get_conditions(row):
    status_keys_list = db.reference('proto/conditions/').get().keys()
    conditions = {}

    '''if row['Hands'] == 1:
        conditions['1H_wielding'] = True
    elif row['Hands'] == 2:
        conditions['2H_wielding'] = True
    else:
        conditions['unarmed'] = True'''

    if row['Status Target'] != '':
        statuses = row['Status Target'].split(',')
        retrieve_status(statuses,status_keys_list,conditions)
    if row['Status Self'] != '':
        statuses = row['Status Self'].split(',')
        retrieve_status(statuses,status_keys_list,conditions)

    #print(conditions)
    return conditions


def abilities_to_dict(dfs):
    abilities = {}
    for df in dfs:
        for i in df.index:
            row = df.loc[i]

            #Remove () from technique
            t_id = row['Way'].split('(')[0]
            if '(' in row['Way']:
                t_id = t_id[:len(t_id)-1]
            
            #Make node_id proper name, with only alphanumerics
            node_id = t_id.lower().replace(' ','_')+"_"+row['Node Name'].replace('-','_')
            icon = path_to_img(row['Action'])
            ability = {
                'aType':row['Type'],
                #'technique':row['Technique'],
                'way':row['Way'],
                'action':int(row['Action Cost']),
                'aim':int(row['Aim']),
                'dmg': split_dmg(row['Damage']),
                'conditions':get_conditions(row),
                'hands':int(row['Hands']),
                'icon': icon,
                'id':node_id,
                'maxRng':int(row['MaxRNG']),
                'minRng':int(row['MinRNG']),
                'name':row['Action'],
                'notes':row['Notes'],
                'skill':row['Skill'],
                'tier':int(row['Tier']),
                'types':get_types(row['Types']),
                'description':row['Description'],
                'size':int(row['Size']),
                'minimum_body':int(row['Minimum Body']),
                'parry_modifier':int(row['Parry Modifier']),
            }
            abilities[node_id] = ability
    return abilities

def dict_to_json(dict, name):
        with open(f'{name}.json','w',encoding='utf-8') as f:
            jresult = json.dumps(dict,indent=2 ,sort_keys=True,ensure_ascii=False)
            f.write(jresult)

def df_to_db(location,dict):
        ref = db.reference(location)
        ref.update(dict)


def remove_itens(dfs):
    item_names = db.reference('proto/items/').get().keys()
    for df in dfs:
        for i in df.index:
            row = df.loc[i]
            if row['Action'] in item_names:
                ref = db.reference(f'proto/items/{row["Action"]}').delete

def update_sheet(names):
    way = get_some_csvs(['Ways'])[0]["id"].tolist()
    gc = connect_spreadsheet()
    sheets = []
    ws = gc.open("Database Spreadsheets")
    ref = db.reference(f'proto/abilities')
    abilities = ref.get()

    for name in names:
        sh = ws.worksheet(name)
        for ability in abilities:
            split = ability.split('_')
            if split[0] in way:
                cell = sh.find(ability['id'])
                print(cell)        


cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'test-692ee.appspot.com',
    'databaseURL' : 'https://test-692ee.firebaseio.com/'
    })
#abilities_to_dict(get_some_csvs(['Unarmed']))
#df_to_db('proto/abilities',abilities_to_dict(get_some_csvs(['Unarmed','Armed','Ranged'])))
#df_to_db('proto/items',weapons_to_dict(get_some_csvs(['Melee Weapons'])))
#remove_itens(get_some_csvs(['Melee Weapons','Missile Weapons']))
update_sheet(["Unarmed"])


'''

def get_weapon_abilities(name):
    pass

def get_itypes(row):
    itypes = {'equipament':True,'item':True,'weapon':True}
    if row['Hands'] == 2:
        itypes['2h'] = True
    return itypes

def weapons_to_dict(dfs):
    weapons = {}
    for df in dfs:
        for i in df.index:
            row = df.loc[i]

            #Remove () from technique
            t_id = row['Technique'].split('(')[0]
            if '(' in row['Technique']:
                t_id = t_id[:len(t_id)-1]
            
            #Make node_id proper name, with only alphanumerics
            node_id = t_id.lower().replace(' ','_')+"_"+row['Node Name'].replace('-','_')
            icon = path_to_img(row['Action'])
            weapons = {
                'abilities':{node_id:True},
                'iTypes':get_itypes(row),
                'icon':icon,
                'name':row['Action'],
                'id':node_id,
                'notes':row['Notes'],
                'qty':1
            }
            weapons[node_id] = weapons
    return weapons

'''