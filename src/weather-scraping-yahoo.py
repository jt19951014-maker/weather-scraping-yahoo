import requests
from bs4 import BeautifulSoup
import pandas as pd

#urlを指定し、htmlを取得
url = "https://weather.yahoo.co.jp/weather/jp/13/4410.html"
response = requests.get(url)

#取得したhtmlをhtml.parserで解析する
soup = BeautifulSoup(response.text, "html.parser")

#取得したい天気全体の要素を取得する
weather_div_all = soup.select_one("#main > div.forecastCity")

#天気情報1つ1つはdivタグに入っているため、divタグの要素を取得し、リストを返す。
weather_div = weather_div_all.select("div")

#天気情報を格納するためのリストを作成
data = []
#1つ1つの天気情報を取得していく
for weather_div in weather_div:
#日付、曜日を取得
    weather_date = weather_div.select("span")
    weather_date,weather_day_of_week = weather_date[0],weather_date[1]

    #天気を取得
    weather_weather = weather_div.find(
        "p", {"class" : "pict"}
    )

    #最高気温の入ったタグを取得
    weather_highest_temperature = weather_div.find(
        "li", {"class" : "high"}
    )
    #実際の最高気温は、タグ中の<em>の要素である
    weather_highest_temperature = weather_highest_temperature.find("em").text

    #最低気温の入ったタグを取得
    weather_lowest_temperature = weather_div.find(
        "li", {"class" : "low"}
    )
    #実際の最低気温は、タグ中の<em>の要素である
    weather_lowest_temperature = weather_lowest_temperature.find("em").text

    data_of_weather = {
        "日付" : weather_date.text,
        "曜日" : weather_day_of_week.text,
        "天気" : weather_weather.text,
        "最高気温" : weather_highest_temperature,
        "最低気温" : weather_lowest_temperature
    }

    data.append(data_of_weather)
#ここまでで、直近2日分のデータ取得。続けてその後6日間のデータを取得していく。



#cssセレクターを指定し全体を取得。
weather_all_of_week = soup.select_one("#yjw_week > table")

#まずは日付、曜日が入った要素を全て取り、リストにする。
weather_date_of_week = weather_all_of_week.find_all(
    "td", {"bgcolor":"#e9eefd"}
)

#続けて天気が入った要素のリストを用意(6日分)
weather_weather_of_week = weather_all_of_week.find_all(
    "td", {"width" : "15%"}
)
#天気以外の要素も取得している。天気の要素はその中の6～12番目。
weather_weather_of_week = weather_weather_of_week[6:12]

#続けて気温が入った要素のリストを用意(6日分)
weather_temperature_of_week = weather_all_of_week.find_all(
    "td", {"width" : "15%"}
)
#気温以外の要素も取得している。気温の要素はその中の13～18番目。
weather_temperature_of_week = weather_temperature_of_week[12:18]

for i in range(6):
    #用意したリストから初日の日付、曜日、天気、最高気温、最低気温を取得する。
    #日付、曜日を取得
    weather_date = weather_date_of_week[i].find("small").contents[0].strip()
    weather_day_of_week = weather_date_of_week[i].find("span").text
    #天気を取得
    weather_weather = weather_weather_of_week[i].text
    #最高気温、最低気温を取得
    weather_highest_temperature = weather_temperature_of_week[i].find("font", {"color" : "#ff3300"}).text
    weather_lowest_temperature = weather_temperature_of_week[i].find("font", {"color" : "#0066ff"}).text

    data_of_weather = {
            "日付" : weather_date,
            "曜日" : weather_day_of_week,
            "天気" : weather_weather,
            "最高気温" : weather_highest_temperature,
            "最低気温" : weather_lowest_temperature
        }

    data.append(data_of_weather)


df = pd.DataFrame(data)

df.to_csv("weather.csv", index = False, encoding="shift-jis")

print("csvファイルを出力しました")
