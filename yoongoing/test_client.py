"""
create(POST), list(GET), delete(DELETE) 요청 테스트하는 파이썬코드
"""

import requests



url = 'http://localhost:8000/create'

#도커 생성
params = {'id':'334434' , 'name':'/busybox1' , 'image':'busybox' , 'port':'8000' , 'command':'test/image1'}
res = requests.post(url=url, params=params)
print(res.text)


url = 'http://localhost:8000/list'
#도커 조회
params = {'id':'334434'}
res = requests.get(url=url, params= params)
print(res.text)


url = 'http://localhost:8000/delete'
#도커 삭제
params = {'id':'334434'}
res = requests.delete(url=url, params= params)
print(res.text)