import requests
from bs4 import BeautifulSoup as bs
from work_with_db import insert_data, getcount

def get_text(url):
    """Функция для получения html странички в виде текста

    Args:
        url (str): ссылка на сайт

    Returns:
        str: html код текстом странички
    """
    r = requests.get(url)
    text=r.text 
    return text
def get_score():
    """Функция для получения оценки с сайта World Art

    Returns:
        list: заполнен оценками по тому порядку, как расположены аниме на сайте
    """    
    list_ = []
    all_text = soup.find_all(attrs={"width": "190", "valign": "top", "align": "center"})
    
    for i in all_text:
        if i.text != '':
            list_.append(i.text[:3])
        else:
            list_.append("-")
    return list_

def get_title_url():
    """Функция для вытаскивания с html кода название и ссылку на аниме

    Returns:
        list_: массив с названиями, по порядку который на сайте
        links: массив с ссылками, по порядку который на сайте
    """    
    list_ = []
    links = []
    all_text = soup.find_all(href=True, attrs={"style": "undeground:none", "class": "h3"})
    for i in all_text:
        if '"' in i.text:
            text = i.text.replace('"', "'") # если в названии есть "", то меняет их на '', чтобы не вызывало ошибок
        else:
            text = i.text
        list_.append(text)
        links.append(f'http://www.world-art.ru/animation/{i["href"]}')
    return list_, links

def get_genre():
    """Функция для получения жанров аниме

    Returns:
        list: содержит массивы, каждый элемент это жанры аниме.
    """    
    list_=[]
    for item in block:
        item = item.text
        i_beg=item.find('Жанры')
        i_end=item.rfind('В основе лежит')
        if i_end==-1:
            i_end=item.rfind("релиз:")-7
        k = item[i_beg:i_end]
        list_.append(k[7:])
    return list_

def get_date():
    """Фукнция для получения даты релиза

    Returns:
        list: содержит даты типа текст
    """    
    list_=[]
    for item in block:
        item = item.text
        i_beg=item.find('Первый релиз')
        i_end=item.rfind('Синопсис: ')
        if i_beg!=-1 & i_end!=-1:
            k = item[i_beg:i_end]
            if '(' in k:
                end=k.rfind('(')
                k = k[:end-1]
            list_.append(k[14:])
    return list_

def get_episode():
    """Функция для получения типа аниме: Полнометражное аниме, ТВ(количество эпизодов) и т.д.

    Returns:
        list: содержит тип аниме
    """    
    list_=[]
    for item in block:
        item = item.text
        i_beg=item.find('Формат аниме')
        i_end=item.rfind('мин.')
        if i_end==-1:
            i_end=item.rfind('базах:')

        k = item[i_beg:i_end]
        if "эп." in k:
            start=k.find('(')
            end=k.find('эп.')
            k = k[start+1:end-1]
        else:
            end=k.find(',')
            if end != -1:
                k = k[14:end]
            else:
                k = k[14:-2]                
        list_.append(k)
    return list_
    
def get_quantity_anime():
    """Функция для получения общего кол-ва аниме с сайта

    Returns:
        int: общее кол-во аниме
    """    
    return int(soup.find_all('td', attrs={'width': '60%'})[0].text[35:])

def remove_spaces(list_):
    """Функция для удаления пустых элементов с массива

    Args:
        list_ (list): массив, имеющий пустые элементы

    Returns:
        list: массив без пустых элементов
    """    
    return [i for i in list_ if i != ""]


num = 0
while True:     
    URL_TEMPLATE = "http://www.world-art.ru/animation/list.php?limit_1="+str(num) # ссылка на сайт
    num += 25 # подставляется в ссылку

    soup = bs(get_text(URL_TEMPLATE), "lxml")
    block = soup.find_all(attrs={"width": "480", "valign": "top", "class": "review"}) # блок со всеми данными об аниме

    if len(block) == 0:
        break
    
    # Ниже создаются все нужные переменные
    titleurl = get_title_url()
    genres = get_genre()
    date = get_date()
    episodes = get_episode()
    title = titleurl[0]
    url = titleurl[1]
    score = get_score()
    quantity = get_quantity_anime()
    all_data = [title, date, score,  genres, episodes, url]
    end_list = list(map(list, zip(*all_data))) # создаётся массив, который наполнен массивами со всеми данными 25-ти аниме. Формат: [["title", "date", "score", "genres", "ep", "url"], [...], [...], ..]

    for i in end_list:
        insert_data(i[0], i[1], i[2], i[3], i[4], i[5])

    count = getcount()[0][0]
    proc = (count * 100) / quantity
    print(f"{'{:.1f}'.format(proc)}%. Это {count} из {quantity} аниме.")
     
print("ГОТОВО!")