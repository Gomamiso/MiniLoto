goto load_html
goto get_test_data

:load_html
python load_html.py -o test_list.csv
goto exit

:get_test_data
python get_html_record.py -i ƒ~ƒjƒƒg_‰ß‹‚Ì’Š‚¹‚ñŒ‹‰Ê_*.html -o test_list.csv
goto exit

:exit