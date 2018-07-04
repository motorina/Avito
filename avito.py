import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime


def get_html(url):
    response = requests.get(url)
    return response.text # возвращает html код страницы (url)


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    tds = soup.find('table', id='currencies-all').find_all('td', class_='currency_name') # здесь лежит объекти СУПА , не ячейки td, а именно объект СУПА
    links = [] #все ссылки (названия - биткоиин, и тд), пока пустой список
    for td in tds:
        a = td.find('a', class_='currency-name-container').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)
    return links 
       

def text_before_word(text, word):
    line = text.split(word)[0].strip()  #strip() удаляет все непечатные символы, табуляция, перенос строки
    return line


def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = text_before_word(soup.find('title').text, 'price')
    except:
        name = ''
    try:
        price = text_before_word(soup.find('div', class_='col-xs-6 col-sm-8 col-md-4 text-left').text, 'USD')
    except:
        price = ''
    data = {'name': name, 
            'price': price}

    return data


def write_csv(i, data):
    with open('coinmarketcap.csv', 'a') as f:    #as f это просто название
        writer = csv.writer(f)
        writer.writerow((data['name'],
                         data['price']))
        print(i, data['name'], 'parsed')


def main():
    start = datetime.now()
    url = 'https://coinmarcet.com/all/views/all'
    all_links = get_all_links(get_html(url)) #возвращает список ссылок со стр
    for i, link in enumerate(all_links):   # enumerate позволяет показывать по мере исполнения нумерация спарсенных ссылок
        html = get_html(link)
        data = get_page_data(html)
        write_csv(i, data)
    end = datetime.now()
    total = end - start
    print(str(total))
    a = input()

if __name__ == '__main__':
    main()
