import time

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


    def find_master(self, page):
        query_params = {
            'l': 'Python',               # language
            'o': 'desc',                 # 排序方式 降序
            'p': str(page),              # 页码
            'q': 'stars:>50',            # 这个参数优先级好像没有l的高
            's': 'stars',                # 排序标准
            'type': 'Repositories',      # 希望得到的返回结果的类型
        }
        body = {
            'commit': 'Follow',
            'utf8': '✓',
        }
        try:
            resp = self.session.get(FIND_URL, params=query_params, cookies=self.session.cookies.get_dict())
        except Exception as e:
            print(str(e))

        tree = etree.HTML(resp.text)
        masters = tree.xpath('//ul[@class="repo-list"]//li//div[1]/h3/a/@href')
        for master in masters:
            mast = master.split('/')[1]
            
            # 要先进入主页 才能拿到在form里面里面hidden的authenticity_token元素的值
            MAST_PROFILE = f'https://github.com/{mast}'
            resp = self.session.get(MAST_PROFILE, cookies=self.session.cookies.get_dict())
            tree = etree.HTML(resp.text)
            auth_tokens = tree.xpath('//span[@class="follow"]//input[@name="authenticity_token"]//@value')
            
            # 如果是组织的话就找不到对应的authenticity_token了
            if not auth_tokens:
                continue
            body.update({'authenticity_token': auth_tokens[0]})

            # 拿到authenticity_token才是关注大佬的操作
            resp = self.session.post(FOLLOW_URL, params={'target': mast}, cookies=self.session.cookies.get_dict(), data=body)
            print('u will follow:', mast, resp.status_code)
            time.sleep(0.5)
            



if __name__ == '__main__':
    USERNAME = input('please enter your github account: \n')
    PASSWORD = input('please enter your github password: \n')
    PAGES = input('enter pages u want to search: \n')
    obj = Github(USERNAME, PASSWORD)
    obj.get_authenticity_token()
    obj.get_session()
    for page in range(1, int(PAGES)+1):
        print('current page is :', page)
        obj.find_master(page)
        time.sleep(0.1)