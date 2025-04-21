from datetime import datetime,date

MAIN_FILE= '/Users/amd/Library/Mobile Documents/com~apple~TextEdit/Documents/main_scraper.txt'
NOW = datetime.now().strftime('%Y-%m-%d')

TODAY=date.today()

def delete_content(main_file):
    with open(main_file,'w') as delete_content:
        delete_content.write('')
    print(f'content of {main_file} has been deleted')

def success_trnsfer(main_file):
    success_message=f'the file {main_file} has been transfered successfully'
    print(success_message)

def trnsfer_data(main_file):
    with open(main_file,'r',encoding='utf-8') as file:
        html = file.read()
    name = ''
    if 'cont-section' in html:
        name = f"autobell/autobell_data/detailed_file/autobell_data_{TODAY}.txt"
        success_trnsfer(main_file)
        delete_content(main_file)
    elif "product-listing" in html:
        name = f"autohub/autuhub_data/detailed_file/autohub_data_{TODAY}1.txt"
        success_trnsfer(main_file)
        delete_content(main_file)

    elif 'search_simple' in html:
        name= f"kcar/kcar_data/detailed_file/kcar_data_{TODAY}_urls.txt"
        success_trnsfer(main_file)
        delete_content(main_file)
    elif 'layout-content' in html:
        name = f"lotte/lotte_detailed_data/detailed_{TODAY}.txt"
        success_trnsfer(main_file)
        delete_content(main_file)
    else:
        print("wasn't successfull")

    with open(name,'w',encoding='utf-8') as f:
        f.write(html)

    

trnsfer_data(MAIN_FILE)

