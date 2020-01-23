from bs4 import BeautifulSoup
import requests
from zhconv import convert
# import pandas as pd
import re
import json
from flask import Flask, Response
from flask_cors import CORS, cross_origin
import os
import time
import calendar

app = Flask(__name__)


def get_page(url):
    response = requests.get(url, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"})
    return response.text

def table_to_data(table):
    data = [[convert(cell.text.strip(), 'zh-cn') for cell in row.find_all("td")] for row in table.find_all("tr")]
    data[0] = [convert(cell.text.strip(), 'zh-cn') for cell in table.find("tr").find_all("th")]
    return data

def normalize_data(data):
    for i in range(1, len(data)):
        row = data[i]
        if 4 == len(row):
            place = row[0]
            date = row[1]
            source = row[3]
            continue
        elif 3 == len(row):
            data[i].insert(0, place)
        elif 2 == len(row):
            if "20" == row[0][:2]:
                data[i].insert(2, source)
                data[i].insert(0, place)
            else:
                data[i][0:0] = (place, date)
        elif 1 == len(row):
            data[i].insert(1, source)
            data[i][0:0] = (place, date)
        else:
            print(row)
        row = data[i]
        place = row[0]
        date = row[1]
        source = row[3]
    return data

def make_confirm_dict(china_data):
    confirm_dict = dict()
    for i in range(len(china_data)):
        place = china_data[i][0]
        desc = china_data[i][2]
        res = re.search('累计[0-9]+例', desc)
        if not res:
            res = re.search('共出现[0-9]+例', desc)
        if not res:
            num_confirmed = 1
        else:
            num_confirmed = int(re.search(r'\d+', res.group()).group())
        confirm_dict[place] = max(num_confirmed, confirm_dict.get(place, 0))
    return confirm_dict

def dict_to_json(confirm_dict):
    res = []
    for k, v in confirm_dict.items():
        # print(k ,v)
        res.append({"name": k, "value": v})
    return res

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
@cross_origin()
def catch_request(path):
    return get_china_data()
    # return Response("<h1>Flask on ZEIT Now</h1><p>You visited: /%s</p>" % (path), mimetype="text/html")
    filename = os.path.join(app.static_folder, 'confirm_china.json')
    print(filename)
    last_mod_time = os.path.getmtime(filename)
    current_time = calendar.timegm(time.gmtime())
    interval_minutes = int((current_time - last_mod_time) / 60)
    print("last modify time: %d, current time: %d, interval_minutes: %d" % (last_mod_time, current_time, interval_minutes))
    if interval_minutes < 15:
        print("gap less than 15 minutes, using cache data")
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return str(data)
    print("gap larger than 15 minutes, fetching latest data")
    data = get_china_data()
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)
    return data


def get_china_data():
    
    # get page
    wiki_url = """https://zh.wikipedia.org/wiki/2019%EF%BC%8D2020%E5%B9%B4%E6%96%B0%E5%9E%8B%E5%86%A0%E7%8B%80%E7%97%85%E6%AF%92%E8%82%BA%E7%82%8E%E4%BA%8B%E4%BB%B6"""
    soup = BeautifulSoup(get_page(wiki_url), 'lxml')

    # get tables
    tables = soup.find_all("table", class_="wikitable")
    china_table = tables[1]

    # convert table to data
    china_data = table_to_data(china_table)
    china_data = normalize_data(china_data)

    # make dict of {place: number of confirmed cases}
    confirm_dict = make_confirm_dict(china_data[1:])  
    # print(confirm_dict)
    # convert dict to json
    confirm_json = json.dumps(dict_to_json(confirm_dict), ensure_ascii=False)
    # print(type(confirm_json))
    # print(confirm_json)
    return confirm_json

# @app.route('/world_data')
# @cross_origin()
# def post_world_data():
#     # get page
#     wiki_url = """https://zh.wikipedia.org/wiki/2019年%EF%BC%8D2020年新型冠狀病毒肺炎事件"""
#     soup = BeautifulSoup(get_page(wiki_url), 'lxml')

#     # get tables
#     tables = soup.find_all("table", class_="wikitable")
#     world_table = tables[0]
#     china_table = tables[1]

#     # convert table to data
#     world_data = table_to_data(world_table)
#     return json.dumps(world_data, ensure_ascii=False)