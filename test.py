"""Test."""
import os
import json
import subprocess
import time
import requests
from datetime import datetime

# urls = [
#     # "https://www.businesstoday.com.tw/",  # bt
#     # "https://www.businessweekly.com.tw/", # bw
#     # "https://csr.cw.com.tw/", # csr
#     # "https://news.cts.com.tw/", # cts
#     # "https://www.msn.com/zh-tw", # msn
#     "https://www.mirrormedia.mg/",  # mm
#     # "https://www.don1don.com/",  # 無每天發文
#     "https://news.pts.org.tw/",  # pts
#     # "https://www.everydayobject.us/",  # 無每天發文
#     # "https://www.ettoday.net/dalemon", # dalemon
#     # "https://www.dramaqueen.com.tw/",  #  dq
#     # "https://applianceinsight.com.tw/",  # 無每天發文
#     # "https://blog.easylife.tw/", # easylife
#     # "https://e-creative.media/", # ecreativemedia
#     # "https://ahui3c.com",  # 無每天發文
#     # "https://anntw.com",  # ann
#     # "https://www.ltn.com.tw/",  # ltn
#     # "https://www.cna.com.tw/postwrite",  # cnamsg
#     # "https://cnews.com.tw",  # cnews
#     # "https://www.coolloud.org.tw",  # cool
#     # "https://www.cool3c.com",  # cool3c
#     # "https://www.cool-style.com.tw/wd2/",  # cools  在網站上看不到頁數，但有在html裡，剛好測試
#     # "https://dailyview.tw",  # dailyview
#     # "https://www.thenewslens.com/",  # tnl
#     # "https://www.twreporter.org/",  # tr
#     # "https://news.ttv.com.tw/",  # ttv
#     # "https://fongnews.net/",   # fong
#     # "https://www.fiftyplus.com.tw/",  # fifty
#     # "https://fgblog.fashionguide.com.tw/content/",  # fgnews
#     # "https://findnewstoday.net/",  # findnewstoday
#     # "https://flipermag.com/",  # flipm
# ]


def es_query(gte, lte, fid, date, time_):
    """es_query."""
    es = "http://104.155.197.221:9201/sm,bbs,news,blog,places/post/_search"
    payload = json.dumps(
        {
            "size": 10000,
            "query": {
                "bool": {
                    "filter": [
                        {
                            "range": {
                                "posttime": {
                                    "gte": gte,
                                    "lte": lte,
                                    "format": "yyyy-MM-dd HH:mm"
                                }
                            }
                        },
                        {
                            "term": {
                                "fid": fid
                            }
                        },
                    ]
                }
            },
        }
    )
    headers = {"'Content-Type'": "'application/json'", "Content-Type": "text/plain"}
    response = requests.request("GET", es, headers=headers, data=payload)
    result = response.json()
    list_ = []
    for i in result["hits"]["hits"]:
        list_.append(i["_source"]["url"])
    with open(f"test_{date}/es_urls_{time_}/es_{fid}.txt", "w") as f:
        json.dump(list_, f)


def compare_files(fid, date, time_):
    """compare_files."""
    with open(f"test_{date}/recursion_{time_}/recursion_{fid}.txt", 'r') as f:
        text = list(map(lambda s: s.replace("\n", ""), f.readlines()))
    set_re = set(text)
    with open(f"test_{date}/es_urls_{time_}/es_{fid}.txt", "r") as f:
        text = f.read()
    set_es = set(json.loads(text))
    compare_set = set_es - set_re
    if compare_set:
        return compare_set
    else:
        return "沒有漏文"


urls = {
    "https://www.mirrormedia.mg/": "mm",
    "https://news.pts.org.tw/": "pts",
    "https://www.ettoday.net/": "et",
    "https://news.ebc.net.tw/": "ettv",
    "https://www.storm.mg/": "st",
    "https://udn.com/news/index": "udn",
}

now = datetime.now()
date = now.strftime("%m%d")
time_ = now.strftime("%m%d_%H%M")
folder_name = f"test_{date}/es_urls_{time_}/"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

for url, fid in urls.items():
    try:
        cmd = f"scrapy crawl recursion -a url={url} -a fid={fid} -a time={time_} -L DEBUG >/dev/null 2>&1 &"
        completed_process = subprocess.run(cmd, shell=True, check=True, stderr=True)
        start = datetime.now().strftime("%Y-%m-%d %H:%M")
        time.sleep(600)
        end = start = datetime.now().strftime("%Y-%m-%d %H:%M")

        es_query(gte=start, lte=end, fid=fid, date=date, time_=time_)
        result = compare_files(fid, date, time_)

        list_ = [
            f"Fid: {fid}\n",
            f"range: {start} - {end}\n",
            f"url: {url}\n",
            "以下漏文\n",
            f"{result}\n",
            f"{'='*60}\n",
        ]
        with open(f"test_{date}/record_{time_}.txt", "a") as f:
            f.writelines(list_)
        # print(f"命令 '{cmd}' 执行成功: {completed_process}")
    except subprocess.CalledProcessError as e:
        print(f"命令 '{cmd}' 执行失败: {e}")
