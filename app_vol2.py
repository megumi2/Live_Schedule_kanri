import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd


#URLから情報を取得
event_url = "http://buglug.jp/live/live-event/"
event = requests.get(event_url)
time.sleep(3)

event_bs = BeautifulSoup(event.text, 'html.parser')

#スケジュールのリンク先を取得
link = event_bs.select(".live-list > ul > a ")
event_link = []
for i in link:
    i = i.get("href")
    event_link.append(i)



title_list = []
place_day_list = []
date_list = []
open_list = []
place_list = []

for i in event_link:
    place_link = requests.get(i)    
    time.sleep(0.5)
    event_bs = BeautifulSoup(place_link.text, 'html.parser')
    place_data_list = event_bs.select(".live-place")
    openlive_data_list =  event_bs.select("p.live-open")
    title_data_list = event_bs.select("h3.title")
    #曜日ごとに分割
    for j in place_data_list:
        place_day_tmp = []
        place_day_text = re.split('\(?[日月火水木金土祝]\)', j.get_text().replace('\r\n', '').replace(' ', '').replace('\n\n', '').replace('\n', '').replace('\u25b6', ' '))
        place_day_list.append(place_day_text)
    for i in title_data_list:
        title_text = i.get_text()
        if len(place_day_text) > 2:
                for m in range(len(place_day_text)-1):
                    title_list.append(title_text)
        else:
            for k in range(len(place_data_list)):
                title_list.append(title_text)

#会場と日程を分けて日程リスト、会場リストにそれぞれ格納

for sublist in place_day_list:
    for element in sublist:
        if not re.search('\d{1,2}日' ,element):
            if len(sublist) > 2:
                for j in range(len(sublist)-1):
                    place_list.append(element)
            else:
                place_list.append(element)           
        else:
            date_list.append(element)

#表にまとめてcsvに出力
event_dict = {'event_date': date_list, 'event_place': place_list, 'live_title': title_list}
event_df = pd.DataFrame(event_dict)
event_df.to_csv('test.csv' ,encoding='cp932' ,index=False, errors='backslashreplace')







