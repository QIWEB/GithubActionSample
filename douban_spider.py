# douban_spider.py
import requests
from bs4 import BeautifulSoup
import sqlite3

def get_movie_list(url):
    headers = {'User-Agent': 'Your User-Agent'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    movie_list = soup.select('.item')
    return movie_list

def save_to_db(movie_list):
    conn = sqlite3.connect('douban_movies.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS movies
                 (title TEXT, rating REAL, link TEXT)''')
    
    for movie in movie_list:
        title = movie.select_one('.title').text.strip()
        rating = float(movie.select_one('.rating_num').text)
        link = 'https://movie.douban.com' + movie.select_one('a')['href']
        c.execute("INSERT INTO movies VALUES (?, ?, ?)", (title, rating, link))
    conn.commit()
    conn.close()

def main():
    base_url = 'https://movie.douban.com/top250'
    for i in range(0, 250, 25):
        url = f'{base_url}?start={i}&filter='
        movie_list = get_movie_list(url)
        save_to_db(movie_list)

if __name__ == '__main__':
    main()
