import requests
from bs4 import BeautifulSoup
import csv
import time

def fetch_weibo_hot_list():
    # 请替换为实际的微博热门页面URL
    url = "https://weibo.com/top/summary"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 检查请求是否成功
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 以下内容假设微博热门列表的HTML结构，实际中需要根据真实页面结构调整
        hot_list_items = soup.select('.hot_list li')  # 假定的CSS选择器
        
        weibo_headlines = []
        for index, item in enumerate(hot_list_items, start=1):
            title_element = item.find('.title')  # 假定的标题元素
            link_element = item.find('a')  # 假定的链接元素
            click_element = item.find('.click')  # 假定的点击量元素
            
            if title_element and link_element:
                title = title_element.text.strip()
                link = link_element['href']
                clicks = click_element.text.strip() if click_element else '未知'
                
                weibo_headlines.append({
                    '序号': index,
                    '标题': title,
                    '详细链接': link,
                    '阅读或点击量': clicks
                })
    
    except Exception as e:
        print(f"Error occurred: {e}")
    
    return weibo_headlines

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['序号', '标题', '详细链接', '阅读或点击量']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in data:
            writer.writerow(row)

if __name__ == "__main__":
    timestamp = int(time.time())
    filename = f"{timestamp}_微博头条.csv"
    hot_list = fetch_weibo_hot_list()
    if hot_list:
        save_to_csv(hot_list, filename)
        print(f"数据已保存至 {filename}")
    else:
        print("未获取到数据")