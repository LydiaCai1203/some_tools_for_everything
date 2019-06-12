"""
今天和黄老师还有欧阳老师一起吃了饭

"""
import requests
from lxml import etree

from config import (
    LOGIN_URL, SESSION_URL, GITHUB_URL, HEADERS, FIND_URL, FOLLOW_URL)


class Github:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def get_authenticity_token(self):
        try:
            resp = self.session.get(LOGIN_URL, headers=HEADERS)
        except Exception as e:
            print(str(e))
        
        html = resp.text
        tree = etree.HTML(html)
        authenticity_token_tag = tree.xpath('//input[@name="authenticity_token"]')[0]
        self.authenticity_token = authenticity_token_tag.xpath('./@value')[0]
        print(self.authenticity_token)
        

    def get_session(self):
        HEADERS.update({
            'Content-Type': 'application/x-www-form-urlencoded',
            'Referer': 'https://github.com/login',
        })
        item = {
            'commit': 'Sign in',
            'utf8': '✓',
            'login': self.username,
            'password': self.password,
            'webauthn-support': 'supported',
            'authenticity_token': self.authenticity_token,
        }
        try:
            resp = self.session.post(SESSION_URL, data=item, headers=HEADERS)
        except Exception as e:
            print(str(e))
        print('your user session is:', '\n')
        print(self.session.cookies.get_dict())


    def find_master(self):
        query_params = {
            'l': 'Python',               # language
            'o': 'desc',                 # 排序方式 降序
            'p': '1',                    # 页码
            'q': 'stars:>50',        # 这个参数优先级好像没有l的高
            's': 'stars',                # 排序标准
            'type': 'Repositories',      # 希望得到的返回结果的类型
        }
        body = {
            'utf8': '✓',
            'authenticity_token': self.authenticity_token,
        }
        try:
            resp = self.session.get(FIND_URL, params=query_params, cookies=self.session.cookies.get_dict())
        except Exception as e:
            print(str(e))
        print(resp.request.url)
        # tree = etree.HTML(resp.text)
        # masters = tree.xpath('//ul[@class="repo-list"]//li//div[1]/h3/a/@href')
        # for master in masters:
        #     mast = master.split('/')[1]
        #     resp = self.session.post(FOLLOW_URL, params={'target': mast}, cookies=self.session.cookies.get_dict(), data=body)
        #     print(resp.status_code)
        #     print(resp.request.url)
        #     print(resp.request.headers)
        #     print(body)

            




if __name__ == '__main__':
    obj = Github(USERNAME, PASSWORD)
    obj.get_authenticity_token()
    obj.get_session()
    obj.find_master()