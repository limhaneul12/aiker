"""
create(POST), list(GET), delete(DELETE) 요청 테스트하는 파이썬코드
"""

import requests



url = 'http://localhost:8000/create_docker'

#도커 생성
params = {'ID':'334435' , 'name':'/busybox2' , 'image':'busybox' , 'port':'8000' , 'command':'test/image2', 'label_idx' : '0'}
res = requests.post(url=url, params=params)
print(res.text)


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