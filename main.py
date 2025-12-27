import requests
from bs4 import BeautifulSoup
import pandas as pd
from fake_useragent import UserAgent
import time
import random

class UniversityRankSpider:
    def __init__(self):
        # 初始化请求头（防反爬）
        self.ua = UserAgent()
        self.headers = {
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.example.com/',  # 替换为目标网站首页
            'Connection': 'keep-alive'
        }
        # 目标网站分页URL模板（需根据实际网站调整，这里以page参数分页为例）
        self.base_url = 'https://www.example.com/university-rank?page={}'  # 替换为真实排名页面URL
        self.total_pages = 30  # 假设每页20条，30页共600条（根据实际分页数量调整）
        self.rank_data = []  # 存储爬取结果

    def get_page_content(self, page_num):
        """获取单页HTML内容"""
        url = self.base_url.format(page_num)
        try:
            # 随机延迟（防反爬）
            time.sleep(random.uniform(1, 3))
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()  # 抛出HTTP请求异常
            response.encoding = response.apparent_encoding  # 自动识别编码
            return response.text
        except Exception as e:
            print(f"获取第{page_num}页失败：{str(e)}")
            return None

    def parse_page(self, html):
        """解析单页HTML，提取高校排名信息"""
        soup = BeautifulSoup(html, 'lxml')
        # 需根据目标网站的HTML结构调整选择器（示例选择器需替换！）
        # 示例：假设排名表格的每一行是 <tr class="rank-item">
        rank_items = soup.select('tr.rank-item')
        
        for item in rank_items:
            try:
                # 提取排名（示例选择器：<td class="rank-num">）
                rank = item.select_one('td.rank-num').get_text(strip=True)
                # 提取学校名称（示例选择器：<td class="university-name">a）
                name = item.select_one('td.university-name a').get_text(strip=True)
                # 提取省份（示例选择器：<td class="province">）
                province = item.select_one('td.province').get_text(strip=True)
                # 提取总分（示例选择器：<td class="total-score">）
                score = item.select_one('td.total-score').get_text(strip=True)
                
                # 存储数据（可根据需要增加字段：类型、特色等）
                self.rank_data.append({
                    '排名': rank,
                    '学校名称': name,
                    '所在省份': province,
                    '总分': score
                })
            except Exception as e:
                print(f"解析单条数据失败：{str(e)}")
                continue

    def save_data(self, filename='国内高校排名600所.csv'):
        """将数据保存为CSV文件"""
        df = pd.DataFrame(self.rank_data)
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"数据保存成功！共{len(self.rank_data)}条记录，文件：{filename}")

    def run(self):
        """启动爬虫"""
        print("开始爬取国内高校排名（共{}页）...".format(self.total_pages))
        for page in range(1, self.total_pages + 1):
            print(f"正在爬取第{page}/{self.total_pages}页...")
            html = self.get_page_content(page)
            if html:
                self.parse_page(html)
        print("爬取完成！")
        self.save_data()

if __name__ == "__main__":
    # 初始化并启动爬虫
    spider = UniversityRankSpider()
    spider.run()
