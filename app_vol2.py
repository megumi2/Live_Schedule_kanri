#!/usr/bin/env python
# coding: utf-8

# In[77]:


import requests
import re
from bs4 import BeautifulSoup
import time
import pandas as pd


# In[78]:


oneman_url = "http://buglug.jp/live/live-oneman/"
event_url = "http://buglug.jp/live/live-event/"


# In[79]:


oneman = requests.get(oneman_url)
event = requests.get(event_url)
time.sleep(3)


# In[80]:


oneman_bs = BeautifulSoup(oneman.text, 'html.parser')
event_bs = BeautifulSoup(event.text, 'html.parser')


# In[81]:


#スケジュールのリンク先を取得
link = event_bs.select(".live-list > ul > a ")
event_link = []
for i in link:
    try:
        i = i.get("href")
        event_link.append(i)
    except:
        pass
print(event_link)


# In[82]:


place = []
etitle = []
place_list = []
ti_list = []
place_2 = []
place_3 = []
date_list = []
list_tmp = []


# In[83]:


for i in range(0, len(event_link)):
    place_link = requests.get(event_link[i])    
    time.sleep(0.5)
    event_bs = BeautifulSoup(place_link.text, 'html.parser')
    place = event_bs.select(".live-place")
    etitle = event_bs.select("h3.title")
    openlive =  event_bs.select("p.live-open")
    for j in place:
        place_tmp = []
        place_text = j.get_text().strip()
        place_tmp.append(place_text)
        place_list.append(place_tmp)
    #ライブタイトルを埋めるために必要な処理        
    for k in etitle:
        etitle = k.get_text()
        for j in place:
            place_tmp_2 = []
            place_text_2 = re.split('\(?[日月火水木金土祝]\)', j.get_text())
            place_tmp_2.append(place_text_2)
            for t in range(len(place_tmp_2[0])-1):
                ti_list.append(etitle)
#曜日を分ける
for sublist in place_list:
    for element in sublist:
        list_tmp.append(re.split('\(?[日月火水木金土祝]\)', element))
#日程を日程リストに、ライブ会場をライブ会場リストに格納させる
for sublist in list_tmp:
    for element in sublist:
        if not re.search('\d{1,2}日' ,element):
            if len(sublist) > 2:
                for j in range(len(sublist)-1):
                    place_3.append(element)
            else:
                place_3.append(element)           
        else:
            date_list.append(element)

#タイトルを取得するぞい


#event_dict = {'event_date': date_list, 'event_place': place_3, 'event_title': ti_list}
#event_df = pd.DataFrame(event_dict)
#event_df


# In[84]:


event_dict = {'event_date': date_list, 'event_place': place_3, 'event_title': ti_list}
event_df = pd.DataFrame(event_dict)
event_df


# In[ ]:




