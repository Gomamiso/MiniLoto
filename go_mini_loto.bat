goto load_html
goto get_test_data

:load_html
python load_html.py -o test_list.csv
goto exit

:get_test_data
python get_html_record.py -i ミニロト_過去の抽せん結果_*.html -o test_list.csv
goto exit

:exit