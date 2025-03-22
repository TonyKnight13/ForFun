import os
import csv
import re
import time
import requests
import urllib3
from bs4 import BeautifulSoup
from urllib.parse import unquote

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# 配置参数
# 深度交流會 同居上下舖 小孩子才做選擇
COMIC_NAME = "小孩子才做選擇"
CSV_FILE = "download_status.csv"
DOWNLOAD_DIR = "downloads"
# BASE_URL = "https://www.wn03.cc"
BASE_URL = "https://www.wnacg01.cc"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["集id", "集文件名", "下载情况"])


def get_downloaded_ids():
    downloaded = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["下载情况"] == "1":
                    downloaded.add(row["集id"])
    return downloaded


def save_status(eid, filename, status):
    # 先检查是否已存在记录
    exists = False
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == str(eid):
                    exists = True
                    break
    if not exists:
        with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([eid, filename, status])

def parse_search_page(page_html):
    soup = BeautifulSoup(page_html, "html.parser")
    items = soup.select("a[href^='/photos-index-aid-']")
    results = []

    for item in items:
        try:
            href = item["href"]
            # 更健壮的ID提取方式
            eid = href.split("-aid-")[1].split(".", 1)[0].strip()
            if not eid.isdigit():
                continue

            # 标题清洗
            title = unquote(item["title"])
            title = re.sub(r'<.*?>', '', title)  # 移除所有HTML标签
            results.append((eid, title))
        except:
            continue

    return results


def get_download_url(eid):
    url = f"{BASE_URL}/download-index-aid-{eid}.html"
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, "html.parser")
        download_btn = soup.select_one(".down_btn.ads")
        if download_btn:
            return download_btn["href"], unquote(download_btn["href"].split("n=")[1])
    except Exception as e:
        print(f"获取下载链接失败: {str(e)}")
    return None, None


def download_file(url, filename):
    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    filepath = os.path.join(DOWNLOAD_DIR, f"{filename}.zip")
    try:
        if url.startswith("//"):
            url = "https:" + url

        with requests.get(url, headers=HEADERS, stream=True, verify=False) as r:
            r.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        print(f"下载失败: {str(e)}")
        return False

def main():
    init_csv()
    downloaded = get_downloaded_ids()
    processed_eids = set()
    page = 1

    while True:
        search_url = f'{BASE_URL}/search/index.php?q={COMIC_NAME}&m=&syn=yes&f=_all&s=create_time_DESC&p={page}'
        print(f"正在处理第 {page} 页...")

        try:
            res = requests.get(search_url, headers=HEADERS)
            res.raise_for_status()
            items = parse_search_page(res.text)

            if not items:
                print("没有更多结果")
                break

            # 本页去重逻辑
            unique_items = []
            seen = set()
            for eid, title in items:
                if eid not in seen:
                    seen.add(eid)
                    unique_items.append((eid, title))

            for eid, title in unique_items:
                # 全局去重检查（CSV记录+本次运行记录）
                if eid in downloaded or eid in processed_eids:
                    continue

                print(f"处理集ID: {eid}")
                dl_url, filename = get_download_url(eid)

                if dl_url and filename:
                    print(f"开始下载: {filename}")
                    success = download_file(dl_url, filename)
                    status = 1 if success else 0
                else:
                    status = 0

                save_status(eid, filename, status)
                processed_eids.add(eid)  # 记录已处理
                time.sleep(2)  # 降低请求频率

            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"发生错误: {str(e)}")
            break


if __name__ == "__main__":
    main()
