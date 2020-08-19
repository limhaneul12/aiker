# What is Aiker?   
<img src="./image/whatisaiker.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="whatisaiker"></img>   

* * *   

# Logic   
1. Create Docker Container   
<img src="./image/logic01.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="createdocker"></img>    

>	docker hub에서 docker image를 다운받아, 웹에서 넘어온 정보를 토대로 docker daemon을 통해 컨테이너 생성.   

2. List Docker Container   
<img src="./image/logic02.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="listdocker"></img>   

>	웹에서 바로 데이터베이스에 접근하여, 생성되어 있는 컨테이너의 리스트 show.   

3. Delete Docker Container   
<img src="./image/logic03.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="deletedocker"></img>   

>	웹에서 바로 데이터베이스에 접근하여, 해당 컨테이너 delete.   

* * *

# Classifier 
<img src="./image/classifier.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="createdocker"></img>

> 도커 컨테이너 200개 생성 기준으로 정확도 96%, loss 0.3 으로 마무리.

# 실행가이드 
실행 전 node js는 12.18.3 npm은 6.14.7 yarn은 1.22.4 버전을 사용했습니다.
1. node js를 설치하여 node js와 npm 설치
2. npm install yarn -g 로 yarn 설치
3. 터미널에 yarn build 입력
4. yarn start 로 시작
5. 주소창에 localhost:8000
6. 메인페이지 (회원가입, 로그인)
<img src="./ui/main.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="main"></img>
<img src="./ui/join.png" width="45%" height="80%" title="px(픽셀) 크기 설정" alt="join"></img>
<img src="./ui/login.png" width="45%" height="80%" title="px(픽셀) 크기 설정" alt="login"></img>

> 메인페이지에서 회원가입과 로그인 하기.

7. search, list 화면
<img src="./ui/main2.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="main2"></img>
<img src="./ui/search.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="search"></img>

> search 버튼을 눌러 list 화면으로 이동

8. create
<img src="./ui/create.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="create"></img>
> 새 컨테이너 등록 버튼을 눌러 정보 입력 후 create 

9. list
<img src="./ui/list.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="list"></img>
> create 한 컨테이너 목록 확인
<img src="./ui/label_list.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="list"></img>
> label 누르면 해당 label에 있는 전체 컨테이너 목록이 보여짐

10. delete
<img src="./ui/list.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="list"></img>
> 컨테이너 목록 오른쪽에 자신이 create한 컨테이너만 삭제 가능

11. 컨테이너 정보 확인
<img src="./ui/컨테이너정보.png" width="90%" height="80%" title="px(픽셀) 크기 설정" alt="컨테이너정보"></img>
> 해당 컨테이너 정보 확인
