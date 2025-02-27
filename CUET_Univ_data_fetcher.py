import requests,json
from bs4 import BeautifulSoup


def extract_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    tables = soup.find_all('table')
    all_tables_data = []
    
    for table in tables:
        headers = [th.text.strip() for th in table.find_all('th')]
        rows = []
        for tr in table.find_all('tr')[1:]:  # Skip the header row
            cells = [td.text.strip() for td in tr.find_all('td')]
            row_data = dict(zip(headers, cells)) if headers else cells
            rows.append(row_data)
        
        all_tables_data.append(rows)
    #print("Succesfully extracted Tables")
    return all_tables_data
    
def get_Univ_Data(url):
    responce = requests.get(url)
    #print(responce.text)
    data = extract_table(responce.text)
    return data
     
with open("Universities.json",'r') as file:
    universities = json.load(file)

for key, value in universities.items():
    for i in range(len(universities[key])):
        url = universities[key][i]["redirectLink"]
        data = get_Univ_Data(url)
        universities[key][i]["cources"] = data
        with open("Universities.json", 'w', encoding='utf-8') as f:
            json.dump(universities, f, indent=4)
            print(f"Successfully Updated University : {universities[key][i]["name"]}({universities[key][i]["type"]}) ({i})")
        

    
        
        
        
        

