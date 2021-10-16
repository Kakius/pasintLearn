import datetime
import os
from os import path
import requests as requests
from bs4 import BeautifulSoup
import lxml

URL = 'https://quotes.toscrape.com'
count = 1


def createDirForParsingFile(example):
    if not path.exists('example_' + example + '/files'):
        os.makedirs('example_' + example + '/files')
        logINfo('Папка создана')
        return
    logINfo('Такая папка уже создана')


def testConnectToURL(url):
    if not url:
        logINfo('Адрес не задан')
        return
    else:
        logINfo('Успешное подключение')
        res = requests.get(url)
        if res.ok:
            return res


def parsing(res):
    global count
    soup = BeautifulSoup(res.text, 'lxml')
    if not soup:
        logINfo('Пустой пакет soup')
        return
    quoteTexts = soup.find_all('span', class_='text')
    quoteAuthors = soup.find_all('small', class_='author')
    quoteTags = soup.find_all('meta', class_='keywords')
    with open('example_1/files/example_' + count.__str__() + '.txt', 'w', encoding='utf-8') as file:
        file.write('Page ' + count.__str__() + '\n')
        i = 0
        while i < len(quoteAuthors):
            author = quoteAuthors[i].text
            file.write('\n' + author + '\n')
            text = quoteTexts[i].text
            file.write(text + '\n')
            tags = quoteTags[i].attrs['content']
            file.write('Tags: ' + tags + '\n')
            i += 1

        logINfo('Файл успешно записан. Имя файла: ' + file.name)
        file.close()
        if soup.find('nav'):
            if soup.find('nav').find('ul', class_='pager'):
                if soup.find('nav').find('ul', class_='pager').find('li', class_='next'):
                    count += 1
                    href = soup.find('nav') \
                        .find('ul', class_='pager') \
                        .find('li', class_='next').find('a')
                    url = URL + href.get('href')
                    res = testConnectToURL(url)
                    parsing(res)


def logINfo(message):
    print('[INFO ' + datetime.datetime.today().__str__() + '] ' + message)


if __name__ == '__main__':
    createDirForParsingFile('1')
    response = testConnectToURL(URL)
    if response:
        parsing(response)
