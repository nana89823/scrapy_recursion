"""es_query."""
import requests
import json
# import subprocess

es = "http://104.155.197.221:9201/sm,bbs,news,blog,places/post/_search"
url = "https://www.chinatimes.com/realtimenews/20231227004425-260405"
fids = ["udn"]
# fids = ["anrpc", "thainr", "rubbernews", "japanrubberweekly", "eurorubberj", "iea", "eia", "reuters", "opec", "cria", "mofcom", "cip", "caam", "arlanxeo", "zeon", "kkpc", "toyota", "volkswagen", "gmotors", "michelin", "continental", "bridgestone", "goodyear"]
gte = "2024-02-02 02:22"
lte = "2024-02-02 02:32"
# gte = '2024-01-29'
# lte = '2024-01-29'
url_list = []
for fid in fids:
    url_list_ = []
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
                                    # "format": "yyyy-MM-dd"
                                }
                            }
                        },
                        {
                            "term": {
                                "fid": fid
                                # "post.id" : "40621f9ce3fbff9cda634d3138cfcf44"
                                #             "url": url
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
    #    print(result["hits"]["total"])
    #     dict_ = {}
    for i in result["hits"]["hits"]:
        # #         if i["_source"]["url"] not in dict_:
        # #             dict_[i["_source"]["url"]] = []
        #         dict_[i["_source"]["url"]].append(i["_source"]["url"])
        #        print(i["_source"]["fetchedtime"])
        #         print(i["_source"]["posttime"])
        # #         print(i["_source"]["post.id"])
        #         print(i["_source"]["title"])
        print(i["_source"]["url"])
        # print(i["_source"]["content"])
        # print("=" * 100)
