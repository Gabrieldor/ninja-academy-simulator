import firebase_admin
from firebase_admin import credentials
import gspread
from google.oauth2 import service_account


def connect_spreadsheet():
    scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
    json_file = "ninja_cred.json"
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc

cred = credentials.Certificate('firebase_cred.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'test-692ee.appspot.com',
    'databaseURL' : 'https://test-692ee.firebaseio.com/'
    })