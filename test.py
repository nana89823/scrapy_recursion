import subprocess
import time

urls = [
    # "https://www.businesstoday.com.tw/",
    # "https://www.businessweekly.com.tw/",
    # "https://csr.cw.com.tw/",
    # "https://news.cts.com.tw/",
    # "https://www.msn.com/zh-tw",
    # "https://www.mirrormedia.mg/",
    # "https://www.don1don.com/",  # 無每天發文
    # "https://news.pts.org.tw/",
    # "https://www.everydayobject.us/",  # 無每天發文
    # "https://www.ettoday.net/dalemon",
    # "https://www.dramaqueen.com.tw/",
    # "https://applianceinsight.com.tw/",  # 無每天發文
    # "https://blog.easylife.tw/",
    # "https://e-creative.media/",
    # "https://ahui3c.com",  # 無每天發文
    # "https://anntw.com",
    # "https://www.ltn.com.tw/",
    # "https://www.cna.com.tw/postwrite",  # cnamsg
    # "https://cnews.com.tw",  # cnews
    # "https://www.coolloud.org.tw",  # cool
    # "https://www.cool3c.com",  # cool3c
    "https://www.cool-style.com.tw/wd2/",  # cools  在網站上看不到頁數，但有在html裡，剛好測試
    "https://dailyview.tw",  # dailyview
    "https://www.thenewslens.com/",  # tnl
    "https://www.twreporter.org/",  # tr
    "https://news.ttv.com.tw/",  # ttv
]

for url in urls:
    try:
        cmd = f"scrapy crawl recursion -a url={url} -L DEBUG >/dev/null 2>&1 &"
        completed_process = subprocess.run(cmd, shell=True, check=True, stderr=True)
        time.sleep(3600)
        print(f"命令 '{cmd}' 执行成功: {completed_process}")
    except subprocess.CalledProcessError as e:
        print(f"命令 '{cmd}' 执行失败: {e}")
