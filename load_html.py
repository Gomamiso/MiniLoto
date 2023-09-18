import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import argparse
import pandas as pd

def Main(args):

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
		output_matrix = AnalyzeTable(table_list)
		if args.output == None:
			for output_vector in output_matrix:
				print(output_vector)
		else:
			df = pd.DataFrame(output_matrix, columns=['ID', '1', '2', '3', '4', '5', '6'])
			# DataFrameをCSVファイルに保存
			df.to_csv(args.output, index=False)

	# ブラウザを閉じる
	browser.quit()
	
	

def AnalyzeTable(table_list):
	output_matrix = []
	for ix, table in enumerate(table_list):
		output_list = []
		for row in table.find_all('tr'):
			cols = row.find_all('th', class_='title', colspan="4")
			if cols != None and len(cols) > 0:
				text = cols[0].get_text()[1:].strip()
				match = re.search(r'第(\d+)回', text)
				if match:
					result = match.group(1)
					output_list.append(int(result))
			cols = row.find_all('th', class_='lotnum')
			if cols != None and len(cols) > 0:
				text = cols[0].get_text()[1:].strip()
				numbers = re.findall(r'\d+', text)
				numbers_list = [int(num) for num in numbers]
				output_list = output_list + numbers_list
		output_matrix.append(output_list)
	return output_matrix
	
if __name__ == "__main__":

	# argv
	parser = argparse.ArgumentParser(description='get record from mini loto result')
	parser.add_argument('-o', '--output', help="Ouput file name", default=None)
	parser.add_argument('-v', '--verbose', help="Use verbose mode", action='store_true')
	args = parser.parse_args()

	Main(args)
	