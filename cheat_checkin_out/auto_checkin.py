import time
import random
import requests

BASE_URL = 'http://106.15.179.143:89/client.do'
USERNAME = 'username'
PASSWORD = 'password'
headers = {
    'User-Agent': 'E-MobileE-Mobile 6.5.68 (iPhone; iOS 10.3.3; zh_CN)',
    'Accept-Language': 'zh-Hans-CN',
    'Accept-Encoding': 'gzip',
}


def get_location(session):
    query_params = {
        'method': 'checkin',
        'type': 'getStatus',
        'sessionkey': None
    }
    cookies = session.cookies.get_dict()
    query_params['sessionkey'] = cookies.get('JSESSIONID')
    resp = session.get(BASE_URL, cookies=cookies, params=query_params)
    data = resp.json()['signbtns'][0]['detail']
    print(data['addr'], data['latitude'], data['longitude'])
    return data['addr'], data['latitude'], data['longitude']


def checkin(session, addr, latitude, longitude):
    query_params = {
        'method': 'checkin',
        'type': 'checkin',
        'latlng': str(latitude) + ',' + str(longitude),
        'addr': addr,
        'sessionkey': None,
    }
    cookies = session.cookies.get_dict()
    query_params['sessionkey'] = cookies.get('JSESSIONID')
    resp = session.get(BASE_URL, cookies=session.cookies.get_dict(), params=query_params)
    return resp.json().get('msg')



def checkout(session, addr, latitude, longitude):
    query_params = {
        'method': 'checkin',
        'type': 'checkout',
        'latlng': str(latitude) + ',' + str(longitude),
        'addr': addr,
        'sessionkey': None,
    }
    cookies = session.cookies.get_dict()
    query_params['sessionkey'] = cookies.get('JSESSIONID')
    resp = session.get(BASE_URL, cookies=session.cookies.get_dict(), params=query_params)
    return resp.json().get('msg')

def login(session):
    query_params = {
        'method': 'getconfig',
        'clientver': '6.5.68',
        'clienttype': 'iPhone',
        'language': 'zh-Hans',
        'country': 'CN',
    }
    resp = session.get(BASE_URL, headers=headers, params=query_params)
    cookies = session.cookies.get_dict()
    body = {
        'loginid': USERNAME,
        'password': PASSWORD,
        'isFromSunEmobile': '1',
    }

    query_params = {
        'method': 'login',
        'udid': '00000000-0000-0000-0000-000000000000',
        'token': None,
        'language': 'zh-Hans',
        'country': 'CN',
        'isneedmoulds': '1',
        'clienttype': 'iPhone',
        'clientver': '6.5.68',
        'clientos': 'iOS',
        'clientosver': '10.3.3',
        'authcode': None,
        'dynapass': None,
        'tokenpass': None,
        'clientChannelId': None,
        'clientuserid': None,
    }
    resp = session.post(BASE_URL, params=query_params, cookies=cookies, headers=headers, data=body)

    if resp.json().get('error'):
        return None
    return 'ok'

def logout(session):
    query_params = {
        'method': 'logout',
        'sessionkey': None,
    }
    cookies = session.cookies.get_dict()
    query_params['sessionkey'] = cookies.get('JSESSIONID')
    resp = session.get(BASE_URL, params=query_params, headers=headers)
    if resp.json().get('error'):
        return None
    return 'ok'
    
def start_cheat():
    session = requests.Session()
    login_result = login(session)
    # addr, latitude, longitude = get_location(session)
    addr, latitude, longitude = '%E4%B8%8A%E6%B5%B7%E5%B8%82%E5%BE%90%E6%B1%87%E5%8C%BA%E8%99%B9%E6%A1%A5%E8%B7%AF%E9%9D%A0%E8%BF%91%E6%B8%AF%E6%B1%87%E6%81%92%E9%9A%86%E5%B9%B%E5%9C%BA', 31.19409478081597, 121.4371006944444
    checkin_result = checkin(session, addr, latitude, longitude)
    # checkout_result = checkout(session, addr, latitude, longitude)
    logout_result = logout(session)
    print('login_result', login_result)
    print(addr, latitude, longitude)
    print('checkin_result', checkin_result)
    print('logout_result', logout_result)  

if __name__ == '__main__':
    sleep_seconds = 60*20
    time.sleep(random.randint(1, sleep_seconds))
    print(sleep_seconds)
    start_cheat()