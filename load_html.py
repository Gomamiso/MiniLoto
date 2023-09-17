import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = webdriver.ChromeOptions()

# ブラウザを起動
browser = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# ウェブページを開く
url = "https://www.takarakujinet.co.jp/miniloto/past.html"
browser.get(url)

# JavaScriptがデータをロードするのを待つ
try:
	# エレメントがロードされるまでの最大待機時間を指定（10秒）
	element = WebDriverWait(browser, 10).until(
		EC.presence_of_element_located((By.ID, "topics-list")) # ここに適切なIDや他の属性を指定
	)
finally:
	# ページのHTMLを取得
	html = browser.page_source

	# BeautifulSoupオブジェクトを作成
	soup = BeautifulSoup(html, 'html.parser')

	# ここでデータを抽出します
	key = 'result table-result-loto'
	table_list = soup.find_all('table', {'class': key})
	for ix, table in enumerate(table_list):
		for row in table.find_all('tr'):
			cols = row.find_all('th', class_='title', colspan="4")
			if cols != None and len(cols) > 0:
				text = cols[0].get_text()[1:].strip()
				match = re.search(r'第(\d+)回', text)
				if match:
					result = match.group(1)
					print(ix,'title:',result)
			cols = row.find_all('th', class_='lotnum')
			if cols != None and len(cols) > 0:
				text = cols[0].get_text()[1:].strip()
				numbers = re.findall(r'\d+', text)
				numbers_list = [int(num) for num in numbers]
				print(ix,'lotnum:',numbers_list)

# ブラウザを閉じる
browser.quit()
