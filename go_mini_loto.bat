goto load_html
goto get_test_data

:load_html
python load_html.py -o data_100.csv -b 100
python load_html.py -o data_200.csv -b 200
goto exit

:get_test_data
python get_html_record.py -i ƒ~ƒjƒƒg_‰ß‹‚Ì’Š‚¹‚ñŒ‹‰Ê_*.html -o test_list.csv
goto exit

:exit