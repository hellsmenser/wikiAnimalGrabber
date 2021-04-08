import requests
from bs4 import BeautifulSoup

#настройка запросв
HOST = 'https://ru.wikipedia.org/'
URL = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}

#запрос к странице вики
def get_html(url, params = ''):
    r = requests.get(url, headers = HEADERS, params = params)
    return r
	
	
#получение данных со страници    
def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='mw-category-group')
    letters = []
    
    for i in items:
        letters.append({
            'letter': i.find('h3').get_text(),
            'title': i.find('ul').get_text().split('\n')
            
        })        
    return letters
	
	
#Запись собранного в файл
def writeAnimals(animals): 
    f = open('Grabber_Output.txt', 'a', encoding="utf-8")
    for i in animals:
        f.write(i + "\n")
    f.close()
	
#основная функция парсера	
def parser():
    html = get_html(URL)
    if(html.status_code == 200):
        animals = [""]
        curlet = 'A'
        oldLet = ''
        while (animals[-1] != 'Zyzzyx chilensis'):
            par = animals[-1].split(" ")
            if(len(par)>1):
                par = par[0] + "+" + par[-1]
            else:
                par = par[0]
            html = get_html(URL, params={'pagefrom':par})
            parcePage = get_content(html.text)
            ind = 0;
            for i in parcePage:   
                if(i['letter'] != curlet):
                    curlet = i['letter']
                animals = i['title']
            if(oldLet != curlet):                
                print(f'Грабим животных на букву {curlet}')                
                oldLet = curlet
            writeAnimals(animals)
                    
        
    else:
        print("ошибка")

#вызов парсера		
result = parser()