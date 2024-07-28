from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
from bs4 import BeautifulSoup
import json
import csv
import pandas as pd

options = Options()
# Запуск браузера с развернутым экраном
options.add_argument('start-maximized')
# Будем использовать браузер Chrom
driver = webdriver.Chrome(options=options)
# Открываем ссылку
driver.get('https://priem.mirea.ru/accepted-entrants-list/')
time.sleep(2)

wait = WebDriverWait(driver, 10)
cards = wait.until(EC.presence_of_all_elements_located((By.XPATH, '//tr[@class="css-bgi5uq"]/following-sibling::tr[1]')))
time.sleep(2)
url_list = [card.find_element(By.XPATH, './td/a').get_attribute('href') for card in cards]


driver2 = webdriver.Chrome(options=options)
wait2 = WebDriverWait(driver2, 15)
books_list = []
print(len(url_list))

i=11

url_item = url_list[i-1]
books_dict = {}



driver2.get(url_item)
time.sleep(20)
try:
        name = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-bco1gb']/b[@class='chakra-text css-1ghp9xx']"))).text
except Exception:
        name = None

try:
        code = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-bco1gb']/i"))).text
except Exception:
        code = None

try:
        places = wait2.until(EC.presence_of_element_located((By.XPATH, "//div[@class='css-1ilqeby']/b"))).text
except Exception:
        places = None
    
    
rows = len(driver2.find_elements(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr'))
    #rows=20
  # подсчет количества столбцов
cols = len(driver2.find_elements(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr[1]/td'))

for r in range(2, rows+1):
        number=driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[1]').text
        snils=driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[2]').text
        priority = driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[3]').text
        bally= driver2.find_element(by=By.XPATH, value = '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr['+str(r)+']/td[11]').text
        #time.sleep(1)
        books_list.append({
            'name': name.strip(),
            'code': code.strip(),
            'places': places.strip(),
            'N': number.strip(),
            'SNILS': snils.strip(),
            'priority': priority.strip(),
            'balls quantity': bally.strip()                      
            })
time.sleep(3)
  # обязательно  прописываем выход из вебдрайвера
driver2.quit()
'''
    snils_list = wait2.until(EC.presence_of_all_elements_located((By.XPATH, '//table[@class="chakra-table css-1tvr1q3"]/tbody/tr')))
   
    for snils in snils_list:
        try:
            #columns = snils.xpath(".//td/text()")
            books_list.append({
            'name': name.strip(),
            'code': code.strip(),
            'places': places.strip(),
  #          '№':columns[0].strip(), 
  #          'СНИЛС': columns[1].strip(),
  #          'Баллы':columns[10].strip()            
            })
        except:
            print('Парсинг закончился с ошибкой!')
'''


df = pd.DataFrame(books_list)
print(df)

df.to_csv('file_resultSS'+str(i)+'.csv', encoding='utf-8-sig')

'''
with open('mirea.json', 'w', encoding='utf-8') as json_file:
    json.dump(books_list, json_file, ensure_ascii=False, indent=4)
'''
'''
json_file = df.to_json (orient='split') 

#export JSON file
with open('my_data.json', 'w') as f:
 f.write(json_file)
 '''
'''
with open('data.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, dialect='excel', delimiter=';')
    writer.writerow(['name', 'code', 'places', 'N', 'SNILS', 'priority', 'balls'])
    writer.writerows(books_list)
    '''