
import json
import csv
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.error import HTTPError


url_spot = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
url_mrt = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"
ptt_url = "https://www.ptt.cc/bbs/Lottery/index.html"


class MRT_and_SPOT():
    @classmethod
    def get_spot_results(cls, url_spot):
        with urlopen(url_spot) as response:
            data = response.read()
            # 抓取"results"之後的內容
            spot_results = json.loads(data).get("data").get("results")
            return spot_results

    @classmethod
    def get_mrt_data(cls, url_mrt):
        with urlopen(url_mrt) as response:
            data = response.read()
            # MRT list => [{'MRT': '文德', 'SERIAL_NO': '2011051800000646', 'address': '臺北市  內湖區內湖路2段175號'}, {'MRT': '中正紀念堂', 'SERIAL_NO': '2011051800000096', 'address': '臺北市  中正區南海路49號'}]
            mrt_data = json.loads(data).get("data")
            # print(mrt_data)
            # district_numbers = {"北投區:["00000000000000000,11111111111111111"]"}
            district_numbers = {}  # 每一區關聯的景點
            mrt_station = {}  # {'大直': ['大直','2011051800000116'],}
            for mrt in mrt_data:
                serial_number = mrt.get('SERIAL_NO')
                district = mrt.get('address').split("  ")[1][:3]  # 取出district
                district_numbers.setdefault(district, []).append(serial_number)

                mrt_station.setdefault(mrt.get("MRT"), [mrt.get("MRT")]).append(
                    mrt.get("SERIAL_NO"))
            return (district_numbers, mrt_station)
            # print(district_numbers)  # {'大安區': ['2011051800000574']}
            # print(mrt_station)

    @classmethod
    def splitURL(cls, strURL):
        imgURL = strURL.split("https://")[1]  # 第0項為空值
        url = "https://" + imgURL
        return url

    @classmethod
    def getDistrict(cls, serial_num, district_numbers):
        for district, number_list in district_numbers.items():
            for num in number_list:
                if num == serial_num:
                    # print(district)
                    return district

    @classmethod
    def get_spot_info(cls, spot_results, mrt_station, district_numbers):
        spots_info = []
        for info in spot_results:
            data = {
                "SpotTitle": info.get("stitle"),
                "District": cls.getDistrict(info.get("SERIAL_NO"), district_numbers),
                "Longitude": info.get("longitude"),
                "Latitude": info.get("latitude"),
                "ImageURL": cls.splitURL(info.get("filelist"))
            }
            for station_nums in mrt_station.values():
                # print(station)
                for i, station_num in enumerate(station_nums):
                    # print(i, station_num)
                    if station_num == info.get("SERIAL_NO"):
                        station_nums[i] = data["SpotTitle"]
                        # print(mrt_station[station][j])

            spots_info.append(data)
        # print(spots_info)
        # print(mrt_station)
        return spots_info

    @classmethod
    def save_spot(cls, spots_info):
        with open("spot.csv", mode="w", encoding="utf-8", newline="") as file:
            fieldnames = ["SpotTitle", "District",
                          "Longitude", "Latitude", "ImageURL"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            for row in spots_info:
                writer.writerow(row)
            print("spot.csv file saved successfully")

    @classmethod
    def save_mrt(cls, mrt_station):
        with open("mrt.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in mrt_station.values():
                writer.writerow(row)
            print("mrt.csv file saved successfully")


class PTT_article():
    article = []

    # create soup
    @classmethod
    def create_soup(cls, ptt_url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        }
        request = Request(ptt_url, headers=headers)
        response = urlopen(request)
        html = response.read().decode("utf-8")
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # 獲得上一頁的頁面
    @classmethod
    def get_previous_page(cls, ptt_url):
        soup = cls.create_soup(ptt_url)
        btns = soup.find_all(class_="btn wide")
        for btn in btns:
            if btn.text == "‹ 上頁":
                previous_page_href = "https://www.ptt.cc/"+btn.get("href")
                # print(previous_page_href)
                return previous_page_href

    # 主要程式碼
    @classmethod
    def get_info(cls, href):
        soup = cls.create_soup(href)
        rent_elements = soup.find_all(class_="r-ent")
        for elements in rent_elements:
            try:
                # print(elements)
                # print("==============================================")
                like = elements.find(
                    class_="hl") if elements.find(class_="hl") else None
                title = elements.find(class_="title").find("a")
                href = "https://www.ptt.cc/" + \
                    title.get("href") if title else None
                if not title:
                    continue

                print(f"Title: {title.text if title else "本文已被刪除"}")
                print(f"Like: {like.text if like else 0}")
                print(f"Href: {href}")
                print(f"日期：{cls.get_date(href)}")

                print("======================================")

                info = {
                    "Title": title.text,
                    "Like": like.text if like else 0,
                    "Date": cls.get_date(href)
                }
                cls.article.append(info)
            except HTTPError as e:
                print(f"Unexcepted error occured: {e}")
                print("======================================")
                continue

    # 獲得日期
    @classmethod
    def get_date(cls, href):
        try:
            next_soup = cls.create_soup(href)
            article_header = next_soup.find_all(class_="article-metaline")
            # print(article_header)
            for article_tag in article_header:

                if article_tag.find(class_="article-meta-tag").text == "時間":
                    date = article_tag.find(class_="article-meta-value").text
                    return date if date else ""
        except HTTPError as e:
            return ""

    @classmethod
    def create_csvFile(cls, articles):
        with open("article.csv", mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["Title", "Like", "Date"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            for row in articles:
                writer.writerow(row)
            print("article.csv saved successfully")


if __name__ == "__main__":
    # Task1
    spot_results = MRT_and_SPOT.get_spot_results(url_spot)
    district_numbers, mrt_station = MRT_and_SPOT.get_mrt_data(url_mrt)
    spots_info = MRT_and_SPOT.get_spot_info(
        spot_results, mrt_station, district_numbers)
    MRT_and_SPOT.save_spot(spots_info)
    MRT_and_SPOT.save_mrt(mrt_station)
    # Task2
    for i in range(1, 4):
        print(f"!!!!!!!!!!!!!!!!!!第{i}頁!!!!!!!!!!!!!!!!!!!!!!!!!!")
        PTT_article.get_info(ptt_url)
        ptt_url = PTT_article.get_previous_page(ptt_url)
        print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
    PTT_article.create_csvFile(PTT_article.article)
