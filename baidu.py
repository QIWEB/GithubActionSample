import requests
from bs4 import BeautifulSoup
import csv

def fetch_baidu_headlines(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    headlines = []
    for news_item in soup.find_all('div', class_='hotnews-item'):
        title = news_item.a.text.strip()
        link = news_item.a['href']
        headlines.append({'title': title, 'link': link})

    print(headlines)
    
    return headlines

def save_to_csv(headlines, filename='baidu_headlines.csv'):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['title', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for headline in headlines:
            writer.writerow(headline)

if __name__ == '__main__':
    url = 'https://news.baidu.com/'
    headlines = fetch_baidu_headlines(url)
    save_to_csv(headlines)
    print("百度头条新闻已成功保存至CSV文件。")