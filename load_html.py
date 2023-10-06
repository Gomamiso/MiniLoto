import re
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
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
		if args.raw == None:
			SaveTableData(args, browser)
		else:
			SaveRawHTML(args, browser)

	# ブラウザを閉じる
	browser.quit()

#--------------------------
def SaveRawHTML(args, browser):
	try:
		html = browser.page_source
		soup = BeautifulSoup(html, 'html.parser')
		table_list = str(soup)
		fn = open(args.raw, 'w', encoding='utf-8')
		fn.write(str(table_list))
		fn.close()
	except Exception as e:
		print(e)
		return False
	return True
	
#--------------------------
def SaveTableData(args, browser):
	print('Start setting page')

	ret = SetupPage(args, browser)
	if ret == False:
		return
	
	print('End setting page')
	
	time.sleep(5)

	print('Start getting table')

	# ページのHTMLを取得
	html = browser.page_source

	# BeautifulSoupオブジェクトを作成
	soup = BeautifulSoup(html, 'html.parser')

	# ここでデータを抽出します
	key = 'result result-classic'
	#key = 'result table-result-loto'
	table_list = soup.find_all('table', {'class': key})

	print('End getting table')

	output_matrix = AnalyzeTableV2(table_list)
	sorted_results = sorted(output_matrix, key=lambda x: x[0])

	print('End Analyzing table:', len(sorted_results))

	#------------------------
	if args.output == None:
		for output_vector in sorted_results:
			print(output_vector)
	else:
		df = pd.DataFrame(sorted_results, columns=['Index', '1', '2', '3', '4', '5', '6'])
		# DataFrameをCSVファイルに保存
		df.to_csv(args.output, index=False)
	return True
	
#--------------------------
def AnalyzeTableV1(table_list):
	output_matrix = []
	for ix, table in enumerate(table_list):
		output_list = []
		for iy, row in enumerate(table.find_all('tr')):
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
	
#--------------------------
def AnalyzeTableV2(table_list):
	output_matrix = []
	for ix, table in enumerate(table_list):
		serial_number = -1
		for iy, row in enumerate(table.find_all('tr')):
			td_text = row.find('td', class_='text-center')
			if td_text != None and len(td_text) > 0:
				td_text = td_text.get_text()
				extracted_number = td_text.split('第')[1].split('回')[0]
				serial_number = int(extracted_number)

			td_tag = row.find('td', class_='text-center text-bold')
			if td_tag != None and len(td_tag) > 0:
				# タグのテキストを取得し、非ブレークスペースと通常のスペースで分割
				numbers_text = td_tag.get_text()
				numbers_list = numbers_text.replace('\u200b', ' ').split()
				# カッコとカッコ内の数字を取り除く
				numbers_list[-1] = numbers_list[-1].strip('()')
				# 数字をスペースで結合して結果を表示
				extracted_numbers = ' '.join(numbers_list)
				data_list = []
				for num in numbers_list:
					try:
						data_list.append(int(num))
					except Exception as e:
						print(e)
				output_matrix.append([serial_number]+data_list)
				serial_number = -1

	return output_matrix

#--------------------------
def SetupPage(args, browser):
	try:
		# ラジオボタンを選択してONにする
		radio_button = browser.find_element_by_css_selector('input[name="jyoken"][value="2"]')
		radio_button.click()
		
		time.sleep(1)
		
		# 'tab-1'ラジオボタンを見つける
		tab1_radio_button = browser.find_element_by_id('tab-1')
		# 'tab-1'ラジオボタンをクリック
		tab1_radio_button.click()

		time.sleep(1)

		# 'select'要素を見つける
		select_element = browser.find_element_by_id('howmany')
		# Selectインスタンスを作成
		select = Select(select_element)
		# 値が'100'のオプションを選択
		select.select_by_value(str(args.size))

		time.sleep(1)

		# 数値をテキストボックスに入力
		text_box = browser.find_element_by_id('round')
		print('begin: %d' % args.begin)
		text_box.send_keys(args.begin + args.size - 1)  # ここで12345という数値を入力しています

		time.sleep(1)

		# '検索'ボタンを見つけてクリック
		search_button = browser.find_element_by_id('search-button')
		search_button.click()

	except Exception as e:
		print(e)
		return False
	return True

def NextPage():
	try:
		# 'pager'クラスを持つ'nav'タグの中の'id=next'要素を見つける
		next_button = driver.find_element_by_css_selector('nav.pager ul#pagination li a#next')
		# 'next'ボタンをクリック
		next_button.click()
	except Exception as e:
		print(e)
		return False
	return True
	
if __name__ == "__main__":

	# argv
	parser = argparse.ArgumentParser(description='get record from mini loto result')
	parser.add_argument('-o', '--output', help="Ouput file name", default=None)
	parser.add_argument('-v', '--verbose', help="Use verbose mode", action='store_true')
	parser.add_argument('-b', '--begin', help="Begin of serial number", type=int, default=1)
	parser.add_argument('-s', '--size', help="Size of serial data", type=int, default=100)
	parser.add_argument('-r', '--raw', help="Raw table's file name", default=None)
	args = parser.parse_args()
	
	error = 0
	if (args.size % 10) != 0 or (args.size / 10) < 1 or (args.size / 10) > 10:
		print('ERROR: size %d == n * 10 and n <= 10' % (args.size))
		error += 1
	if args.begin < 1:
		print('ERROR: begin %d' % (args.begin))
		error += 1

	if error == 0:
		Main(args)
	