import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()

# ウェブドライバーのパスを設定します（あなたのシステムによって異なります）
#path_to_webdriver = 'C:/Program Files (x86)/Google/Chrome/Application/114.0.5735.90/chromedriver.exe'

# ブラウザを起動
#browser = webdriver.Chrome(executable_path=path_to_webdriver)
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# ウェブページを開く
url = "https://www.takarakujinet.co.jp/miniloto/past.html"
browser.get(url)

# JavaScriptがデータをロードするのを待つ（時間を調整するか、より洗練された待機方法を使用するかもしれません）
time.sleep(10)

# ページのHTMLを取得
html = browser.page_source

# BeautifulSoupオブジェクトを作成
soup = BeautifulSoup(html, 'html.parser')


# ここでデータを抽出します（具体的な抽出方法は、ページの構造に依存します）
# 例えば、テーブルのデータを抽出する場合のコード：
key = 'result table-result-loto'
table_list = soup.find_all('table', {'class': key})
for ix, table in enumerate(table_list):
	print(ix, table)

'''
table = soup.find('table', {'class': key})

if table:
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        cols = [col.get_text(separator=' ').strip() for col in cols]
        print(cols)
else:
    print("Table not found")
'''

# ブラウザを閉じる
browser.quit()
