import subprocess

urls = [
    "https://www.don1don.com/",
    "https://news.pts.org.tw/",
    "https://www.everydayobject.us/",
    "https://www.ettoday.net/dalemon",
    "https://www.dramaqueen.com.tw/",
    "https://applianceinsight.com.tw/",
    "https://blog.easylife.tw/",
    "https://e-creative.media/",
    "https://ahui3c.com",
    "https://anntw.com",
    "https://www.ltn.com.tw/",
]

for url in urls:
    try:
        cmd = f"scrapy crawl recurison -a url={url} -L DEBUG >/dev/null 2>&1 &"
        completed_process = subprocess.run(cmd, shell=True, check=True, stderr=True)
        print(f"命令 '{cmd}' 执行成功: {completed_process}")
    except subprocess.CalledProcessError as e:
        print(f"命令 '{cmd}' 执行失败: {e}")
