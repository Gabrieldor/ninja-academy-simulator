import ninja_login as login
from firebase_admin import storage
from firebase_admin import db
import pandas as pd
import json

def path_to_img(name):
    bucket = storage.bucket()
    blob = bucket.get_blob(f'abilities_icons/{name}.png')
    if blob is not None:
        path = 'https://firebasestorage.googleapis.com/v0' + blob.path + '?alt=media&token=' + blob.metadata['firebaseStorageDownloadTokens']
        return path
    else:
        return 'resources/img/missing.png'

def get_csvs(*names):
    dfs = []
    gc = login.connect_spreadsheet()
    spreadsheet = gc.open("Database Spreadsheets")
    for name in names:
        sheet = spreadsheet.worksheet(name)
        dados = sheet.get_all_records()
        df = pd.DataFrame(dados)
        dfs.append(df)
    return dfs

def dict_to_json(dict, name):
        with open(f'{name}.json','w',encoding='utf-8') as f:
            jresult = json.dumps(dict,indent=2 ,sort_keys=True,ensure_ascii=False)
            f.write(jresult)

def dict_to_db(location,dict):
        ref = db.reference(location)
        ref.update(dict)













