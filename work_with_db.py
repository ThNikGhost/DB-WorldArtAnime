import sqlite3
conn = sqlite3.connect('.\DB-all-anime.db')
cursor = conn.cursor()


def sql(text: str):
    """Упрощает ввод комант

    Args:
        text (str): Текст формата sql
    """    
    try:
        cursor.execute(text)
    except Exception as e:
        print(text)
        print(e)

def getcount():
    """Упрощает получения кол-ва аниме в БД

    Returns:
        str: кол-во аниме в БД
    """    
    sql(f"SELECT count() FROM Anime")
    return cursor.fetchall()    

def insert_data(titles, dates, scores, genres, episodes, url):
    """Упрощает ввод данных в БД

    Args:
        titles (str): Название аниме
        dates (str): Дата выхода аниме
        scores (str): Оценка аниме с сайта
        genres (str): Жанр аниме
        episodes (str): кол-во эпизодов, если они есть, иначе тип аниме(полнометражное аниме и т.д.)
        url (str): ссылка на аниме
    """    
    sql(f"""INSERT INTO Anime (
                        Title,
                        [release date],
                        Score,
                        Genres,
                        episode,
                        url
                    )
                    VALUES (
                        "{titles}",
                        "{dates}",
                        "{scores}",
                        "{genres}",
                        "{episodes}",
                        "{url}"
                    );
    """)
    conn.commit()
