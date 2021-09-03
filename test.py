from keras.models import Sequential
from keras.layers import Dense
import numpy as np
import ast
from keras.datasets import boston_housing
                                            #pip install keras
                                            #pip install tensorflow
import codecs
import json
import csv
from tensorflow import keras
from flask import Flask
from flask import request
from urllib.parse import unquote
#json_r = {"POLICY_ID": "13", "POLICY_BEGIN_MONTH": "1","POLICY_END_MONTH": "1","POLICY_SALES_CHANNEL": "39","POLICY_SALES_CHANNEL_GROUP": "1","POLICY_BRANCH": "Москва","POLICY_MIN_AGE": "51","POLICY_MIN_DRIVING_EXPERIENCE": "12","VEHICLE_MAKE": "Land Rover","VEHICLE_MODEL": "Discovery","VEHICLE_ENGINE_POWER": "245","VEHICLE_IN_CREDIT": "0","VEHICLE_SUM_INSURED": "1283202","POLICY_INTERMEDIARY": "856","INSURER_GENDER": "F","POLICY_CLM_N": "0","POLICY_CLM_GLT_N": "0","POLICY_PRV_CLM_N": "N","POLICY_PRV_CLM_GLT_N": "N","CLIENT_HAS_DAGO": "1","CLIENT_HAS_OSAGO": "0","POLICY_COURT_SIGN": "0","CLAIM_AVG_ACC_ST_PRD": "0"," POLICY_HAS_COMPLAINTS": "0","POLICY_YEARS_RENEWED_N": "0","POLICY_DEDUCT_VALUE": "0","CLIENT_REGISTRATION_REGION": "Тульская","POLICY_PRICE_CHANGE": "-0.29" }
#http://127.0.0.1:5000/?json={%22POLICY_ID%22:%20%2213%22,%20%22POLICY_BEGIN_MONTH%22:%20%221%22,%22POLICY_END_MONTH%22:%20%221%22,%22POLICY_SALES_CHANNEL%22:%20%2239%22,%22POLICY_SALES_CHANNEL_GROUP%22:%20%221%22,%22POLICY_BRANCH%22:%20%22%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%22,%22POLICY_MIN_AGE%22:%20%2251%22,%22POLICY_MIN_DRIVING_EXPERIENCE%22:%20%2212%22,%22VEHICLE_MAKE%22:%20%22Land%20Rover%22,%22VEHICLE_MODEL%22:%20%22Discovery%22,%22VEHICLE_ENGINE_POWER%22:%20%22245%22,%22VEHICLE_IN_CREDIT%22:%20%220%22,%22VEHICLE_SUM_INSURED%22:%20%221283202%22,%22POLICY_INTERMEDIARY%22:%20%22856%22,%22INSURER_GENDER%22:%20%22F%22,%22POLICY_CLM_N%22:%20%220%22,%22POLICY_CLM_GLT_N%22:%20%220%22,%22POLICY_PRV_CLM_N%22:%20%22N%22,%22POLICY_PRV_CLM_GLT_N%22:%20%22N%22,%22CLIENT_HAS_DAGO%22:%20%221%22,%22CLIENT_HAS_OSAGO%22:%20%220%22,%22POLICY_COURT_SIGN%22:%20%220%22,%22CLAIM_AVG_ACC_ST_PRD%22:%20%220%22,%22%20POLICY_HAS_COMPLAINTS%22:%20%220%22,%22POLICY_YEARS_RENEWED_N%22:%20%220%22,%22POLICY_DEDUCT_VALUE%22:%20%220%22,%22CLIENT_REGISTRATION_REGION%22:%20%22%D0%A2%D1%83%D0%BB%D1%8C%D1%81%D0%BA%D0%B0%D1%8F%22,%22POLICY_PRICE_CHANGE%22:%20%22-0.29%22,%20%22POLICY_HAS_COMPLAINTS%22:%20%22123%22%20%20}
from flask import jsonify

f = codecs.open('db.txt', 'r', "utf_8_sig")
ff = f.read()
items = ast.literal_eval(ff)


def tex_to_int(st):
    text = ":".join("{:02x}".format(ord(c)) for c in st)
    return ''.join(str(int(h, 16)) for h in text.split(':'))

def correct_data(row):
    if row[5] == 'Moscow':
        row[5] = '1'
    elif row[5] == 'Petersburg':
        row[5] = '2'

##################################
    if row[14] == 'M':
        row[14] = '0'
    elif row[14] == 'F':
        row[14] = '1'

##################################
    row[8] = items[0][row[8]]
    row[9] = items[1][row[9]]
    row[26] = items[2][row[26]]
    # if row[27] == "N":
    #     row[27] = '-1'
    if row[24] == "N":
        row[24] = '-1'
##################################
    if row[13] == 'N':
        row[13] = '-1'

###################################
    row[15] = tex_to_int(row[15])
    row[16] = tex_to_int(row[16])
    row[17] = tex_to_int(row[17])
    row[18] = tex_to_int(row[18])


    return row



def prediction(test):

    #test = ['13', '1', '1', '54', '6', 'Москва', '30', '8', 'Volkswagen', 'Tiguan', '170', '0', '1063335', '352', 'F', '1S', '1S', '0', '0', '1', '1', '0', '2', '0', '1', '0', 'Москва', '-0.29']
    #test = ['62', '8', '8', '29', '1', 'Санкт-Петербург','42','18','Dodge','Grand Caravan','215','0','300571','374','M','0','0','0','0','0','1','0','0','0','1','0','Санкт-Петербург','-1.00']
    x = correct_data(test)
    x = np.array(x, float)
    #
    #
    #
    mean = x.mean(axis=0)
    std = x.std(axis=0)
    x -= mean
    x /= std
    #
    x_test = np.array([x], float)
    # print(x_test)
    model = Sequential()
    #
    model = keras.models.load_model('16_model_2.h5')
    #
    pred = model.predict(x_test)
    return str(pred[0][0])


app = Flask(__name__)
@app.route('/', methods = ['POST'])
def hello():
   #json_r = {"POLICY_ID": "13", "POLICY_BEGIN_MONTH": "1","POLICY_END_MONTH": "1","POLICY_SALES_CHANNEL": "39","POLICY_SALES_CHANNEL_GROUP": "1","POLICY_BRANCH": "Москва","POLICY_MIN_AGE": "51","POLICY_MIN_DRIVING_EXPERIENCE": "12","VEHICLE_MAKE": "Land Rover","VEHICLE_MODEL": "Discovery","VEHICLE_ENGINE_POWER": "245","VEHICLE_IN_CREDIT": "0","VEHICLE_SUM_INSURED": "1283202","POLICY_INTERMEDIARY": "856","INSURER_GENDER": "F","POLICY_CLM_N": "0","POLICY_CLM_GLT_N": "0","POLICY_PRV_CLM_N": "N","POLICY_PRV_CLM_GLT_N": "N","CLIENT_HAS_DAGO": "1","CLIENT_HAS_OSAGO": "0","POLICY_COURT_SIGN": "0","CLAIM_AVG_ACC_ST_PRD": "0"," POLICY_HAS_COMPLAINTS": "0","POLICY_YEARS_RENEWED_N": "0","POLICY_DEDUCT_VALUE": "0","CLIENT_REGISTRATION_REGION": "Тульская","POLICY_PRICE_CHANGE": "-0.29" }
   #http://192.168.0.102:5000/?POLICY_ID=1&POLICY_BEGIN_MONTH=11&POLICY_END_MONTH=2&POLICY_SALES_CHANNEL=39&POLICY_SALES_CHANNEL_GROUP=6&POLICY_BRANCH=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0&POLICY_MIN_AGE=51&POLICY_MIN_DRIVING_EXPERIENCE=7&VEHICLE_MAKE=Kia&VEHICLE_MODEL=Logan&VEHICLE_ENGINE_POWER=245&VEHICLE_IN_CREDIT=0&VEHICLE_SUM_INSURED=453000&POLICY_INTERMEDIARY=641&INSURER_GENDER=F&POLICY_CLM_N=0&POLICY_CLM_GLT_N=0&POLICY_PRV_CLM_N=0&POLICY_PRV_CLM_GLT_N=0&CLIENT_HAS_DAGO=1&CLIENT_HAS_OSAGO=0&POLICY_COURT_SIGN=0&CLAIM_AVG_ACC_ST_PRD=0&POLICY_HAS_COMPLAINTS=0&POLICY_YEARS_RENEWED_N=0&POLICY_DEDUCT_VALUE=0&CLIENT_REGISTRATION_REGION=Тульская&POLICY_PRICE_CHANGE=-0.29

    #if len(request.args.get('json')) == 0:
    #    json_r = "None"
    #    return json_r
    #else:
    #json_r = request.args.get('json')















    # url = unquote(json_r)
    # print(url)
    #
    #
    #
    # str_get = json.loads(json_r)


    # POLICY_ID = str_get["POLICY_ID"]
    # POLICY_BEGIN_MONTH = str_get["POLICY_BEGIN_MONTH"]
    # POLICY_END_MONTH = str_get["POLICY_END_MONTH"]
    # POLICY_SALES_CHANNEL = str_get["POLICY_SALES_CHANNEL"]
    # POLICY_SALES_CHANNEL_GROUP = str_get["POLICY_SALES_CHANNEL_GROUP"]
    # POLICY_BRANCH = str_get["POLICY_BRANCH"]
    # POLICY_MIN_AGE = str_get["POLICY_MIN_AGE"]
    # POLICY_MIN_DRIVING_EXPERIENCE = str_get["POLICY_MIN_DRIVING_EXPERIENCE"]
    # VEHICLE_MAKE = str_get["VEHICLE_MAKE"]
    # VEHICLE_MODEL = str_get["VEHICLE_MODEL"]
    # VEHICLE_ENGINE_POWER = str_get["VEHICLE_ENGINE_POWER"]
    # VEHICLE_IN_CREDIT = str_get["VEHICLE_IN_CREDIT"]
    # VEHICLE_SUM_INSURED = str_get["VEHICLE_SUM_INSURED"]
    # POLICY_INTERMEDIARY = str_get["POLICY_INTERMEDIARY"]
    # INSURER_GENDER = str_get["INSURER_GENDER"]
    # POLICY_CLM_N = str_get["POLICY_CLM_N"]
    # POLICY_CLM_GLT_N = str_get["POLICY_CLM_GLT_N"]
    # POLICY_PRV_CLM_N = str_get["POLICY_PRV_CLM_N"]
    # POLICY_PRV_CLM_GLT_N = str_get["POLICY_PRV_CLM_GLT_N"]
    # CLIENT_HAS_DAGO = str_get["CLIENT_HAS_DAGO"]
    # CLIENT_HAS_OSAGO = str_get["CLIENT_HAS_OSAGO"]
    # POLICY_COURT_SIGN = str_get["POLICY_COURT_SIGN"]
    # CLAIM_AVG_ACC_ST_PRD = str_get["CLAIM_AVG_ACC_ST_PRD"]
    # POLICY_HAS_COMPLAINTS = str_get["POLICY_HAS_COMPLAINTS"]
    # POLICY_YEARS_RENEWED_N = str_get["POLICY_YEARS_RENEWED_N"]
    # POLICY_DEDUCT_VALUE = str_get["POLICY_DEDUCT_VALUE"]
    # CLIENT_REGISTRATION_REGION = str_get["CLIENT_REGISTRATION_REGION"]
    # POLICY_PRICE_CHANGE = str_get["POLICY_PRICE_CHANGE"]
    check = True
    POLICY_ID = request.get_json().get("POLICY_ID")
    if POLICY_ID is None:
        print("POLICY_ID")
        check = False
    POLICY_BEGIN_MONTH = request.get_json().get("POLICY_BEGIN_MONTH")
    if POLICY_BEGIN_MONTH is None:
        print("POLICY_BEGIN_MONTH")
        check = False
    POLICY_END_MONTH = request.get_json().get("POLICY_END_MONTH")
    if POLICY_END_MONTH is None:
        print("POLICY_END_MONTH")
        check = False
    POLICY_SALES_CHANNEL = request.get_json().get("POLICY_SALES_CHANNEL")
    if POLICY_SALES_CHANNEL is None:
        print("POLICY_SALES_CHANNEL")
        check = False
    POLICY_SALES_CHANNEL_GROUP = request.get_json().get("POLICY_SALES_CHANNEL_GROUP")
    if POLICY_SALES_CHANNEL_GROUP is None:
        print("POLICY_SALES_CHANNEL_GROUP")
        check = False
    POLICY_BRANCH = request.get_json().get("POLICY_BRANCH")
    if POLICY_BRANCH is None:
        print("POLICY_BRANCH")
        check = False
    POLICY_MIN_AGE = request.get_json().get("POLICY_MIN_AGE")
    if POLICY_MIN_AGE is None:
        print("POLICY_MIN_AGE")
        check = False
    POLICY_MIN_DRIVING_EXPERIENCE = request.get_json().get("POLICY_MIN_DRIVING_EXPERIENCE")
    if POLICY_MIN_DRIVING_EXPERIENCE is None:
        print("POLICY_MIN_DRIVING_EXPERIENCE")
        check = False
    VEHICLE_MAKE = request.get_json().get("VEHICLE_MAKE")
    if VEHICLE_MAKE is None:
        print("VEHICLE_MAKE")
        check = False
    VEHICLE_MODEL = request.get_json().get("VEHICLE_MODEL")
    if VEHICLE_MODEL is None:
        print("VEHICLE_MODEL")
        check = False
    VEHICLE_ENGINE_POWER = request.get_json().get("VEHICLE_ENGINE_POWER")
    if VEHICLE_ENGINE_POWER is None:
        print("VEHICLE_ENGINE_POWER")
        check = False
    VEHICLE_IN_CREDIT = request.get_json().get("VEHICLE_IN_CREDIT")
    if VEHICLE_IN_CREDIT  is None:
        print("VEHICLE_IN_CREDIT")
        check = False
    VEHICLE_SUM_INSURED = request.get_json().get("VEHICLE_SUM_INSURED")
    if VEHICLE_SUM_INSURED is None:
        print("VEHICLE_SUM_INSURED")
        check = False
    POLICY_INTERMEDIARY = request.get_json().get("POLICY_INTERMEDIARY")
    if POLICY_INTERMEDIARY is None:
        print("POLICY_INTERMEDIARY")
        check = False
    INSURER_GENDER = request.get_json().get("INSURER_GENDER")
    if INSURER_GENDER is None:
        print("INSURER_GENDER")
        check = False
    POLICY_CLM_N = request.get_json().get("POLICY_CLM_N")
    if POLICY_CLM_N  is None:
        print("POLICY_CLM_N")
        check = False
    POLICY_CLM_GLT_N = request.get_json().get("POLICY_CLM_GLT_N")
    if POLICY_CLM_GLT_N is None:
        print("POLICY_CLM_GLT_N")
        check = False
    POLICY_PRV_CLM_N = request.get_json().get("POLICY_PRV_CLM_N")
    if POLICY_PRV_CLM_N is None:
        print("POLICY_PRV_CLM_N")
        check = False
    POLICY_PRV_CLM_GLT_N = request.get_json().get("POLICY_PRV_CLM_GLT_N")
    if POLICY_PRV_CLM_GLT_N is None:
        print("POLICY_PRV_CLM_GLT_N")
        check = False
    CLIENT_HAS_DAGO = request.get_json().get("CLIENT_HAS_DAGO")
    if CLIENT_HAS_DAGO is None:
        print("CLIENT_HAS_DAGO")
        check = False
    CLIENT_HAS_OSAGO = request.get_json().get("CLIENT_HAS_OSAGO")
    if CLIENT_HAS_OSAGO is None:
        print("CLIENT_HAS_OSAGO")
        check = False
    POLICY_COURT_SIGN = request.get_json().get("POLICY_COURT_SIGN")
    if POLICY_COURT_SIGN  is None:
        print("POLICY_COURT_SIGN")
        check = False
    CLAIM_AVG_ACC_ST_PRD = request.get_json().get("CLAIM_AVG_ACC_ST_PRD")
    if CLAIM_AVG_ACC_ST_PRD is None:
        print("CLAIM_AVG_ACC_ST_PRD")
        check = False
    POLICY_HAS_COMPLAINTS = request.get_json().get("POLICY_HAS_COMPLAINTS")
    if POLICY_HAS_COMPLAINTS is None:
        print("POLICY_HAS_COMPLAINTS")
        check = False
    POLICY_YEARS_RENEWED_N = request.get_json().get("POLICY_YEARS_RENEWED_N")
    if POLICY_YEARS_RENEWED_N is None:
        print("POLICY_YEARS_RENEWED_N")
        check = False
    POLICY_DEDUCT_VALUE = request.get_json().get("POLICY_DEDUCT_VALUE")
    if POLICY_DEDUCT_VALUE is None:
        print("POLICY_DEDUCT_VALUE")
        check = False
    CLIENT_REGISTRATION_REGION = request.get_json().get("CLIENT_REGISTRATION_REGION")
    if CLIENT_REGISTRATION_REGION is None:
        print("CLIENT_REGISTRATION_REGION")
        check = False
    POLICY_PRICE_CHANGE = request.get_json().get("POLICY_PRICE_CHANGE")
    if POLICY_PRICE_CHANGE is None:
        print("POLICY_PRICE_CHANGE")
        check = False
    if check:
        arr = [POLICY_ID, POLICY_BEGIN_MONTH, POLICY_END_MONTH, POLICY_SALES_CHANNEL, POLICY_SALES_CHANNEL_GROUP, POLICY_BRANCH, POLICY_MIN_AGE, POLICY_MIN_DRIVING_EXPERIENCE, VEHICLE_MAKE, VEHICLE_MODEL, VEHICLE_ENGINE_POWER, VEHICLE_IN_CREDIT, VEHICLE_SUM_INSURED, POLICY_INTERMEDIARY, INSURER_GENDER, POLICY_CLM_N,POLICY_CLM_GLT_N, POLICY_PRV_CLM_N, POLICY_PRV_CLM_GLT_N, CLIENT_HAS_DAGO, CLIENT_HAS_OSAGO, POLICY_COURT_SIGN, CLAIM_AVG_ACC_ST_PRD, POLICY_HAS_COMPLAINTS, POLICY_YEARS_RENEWED_N, POLICY_DEDUCT_VALUE, CLIENT_REGISTRATION_REGION, POLICY_PRICE_CHANGE]


        o = prediction(arr)
        return  jsonify({"res" : o})
    else:
        return "No parametrs"




if __name__ == "__main__":
    app.run(host="0.0.0.0")