#-*-condig:utf-8-*-

"""
create(POST), list(GET), delete(DELETE) 요청 테스트하는 파이썬코드
"""

import requests
import urllib.parse

url = 'http://192.168.0.23:8000/create_docker'

#도커 생성

while True:
    image = urllib.parse.unquote(input("image >"))
    command = urllib.parse.unquote(input("command >"))

    params = {'name': input("name >"), 'image': image,
              'port': '8000', 'command': command,
              'label_idx': 1, 'user_idx': 1}
    res = requests.post(url=url, params=params)
    print(res.text)

    continue_ = input("continue> >")
    if continue_ in ["No", "n", "no", "exit", "false"]:
        break
    # 계속 할시 list에 담아두고 계속 생성
    elif continue_ in ["yes", "y"]:
        continue




# url = 'http://localhost:8000/list'
# #도커 조회
# params = {'id':'334434'}
# res = requests.get(url=url, params= params)
# print(res.text)
#
#
# url = 'http://localhost:8000/delete'
# #도커 삭제
# params = {'id':'334434'}
# res = requests.delete(url=url, params= params)
# print(res.text)
