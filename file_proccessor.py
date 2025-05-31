import json
from datetime import date


TODAY = date.today()

class FileProccessing:
    def read_text_file(self,text_file):
        with open(text_file,encoding='utf-8') as file:
            return file.read()
        
    def read_json_file(self,json_file):
        with open(json_file, encoding='utf-8') as json_file:
            return json.load(json_file)
    
    def export_json(self,data:dict,output_json):
        with open(output_json,'w',encoding='utf-8') as j:
            d= json.dumps(data,ensure_ascii=False,indent=4)
            j.write(d)
            print('File exported successfully')

    def save_html_elements(self,output_text_file,results):
        with open(f"{output_text_file}.txt", 'w', encoding='utf-8') as f:
            for result in results:
                f.write(str(result) + '\n')

    


    

    



        


