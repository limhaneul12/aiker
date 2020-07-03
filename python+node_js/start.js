const express = require('express')
const app = express()

app.get('/', (req, res) => {
    // child_process 라는 라이브러리 npm에 다운받음
    const { spawn } = require('child_process');
    const pyProg = spawn('python', ['docker_preprocessing.py']);
    // python 사용한다고 선언후 [docker_preprocessing.py] <- 경로 설정 해주어야함 
    /*
    EX)
    spawn('python', ['/home/sky81219/PycharmProjects/Deeplearning/docker_prepro/docker_preprocessing.py']);
     */
    pyProg.stdout.on('data', function(data) {
    /*
     데이터 받고 출력해주는곳 
     일단 간단한 테스트여서 이게 원본이 될 수 있다는 보장은 없음 
     해댕본이 자기랑 맞는지 확인 후 재구성 바람 
     */
        console.log(data.toString()); // 데이터 출력 
        res.write(data);
        res.end('end'); // 데이터 출력이 다 끝나면 end
    });
})

app.listen(4000, () => console.log('Application listening on port 4000!'))
