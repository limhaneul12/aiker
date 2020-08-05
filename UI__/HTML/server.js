/** * 웹 서버에 html 파일 서비스 하기 */ 
//var http = require('http'); 
var express = require('express');
var fs = require('fs'); // 파일 읽기, 쓰기 등 을 할 수 있는 모듈 // 404 error message : 페이지 오류가 발생했을때, 
var app = express();
var port = 3000;
/*function send404Message(response){ 
	response.writeHead(404,{"Content-Type":"text/plain"}); // 단순한 글자 출력 
	response.write("404 ERROR... "); 
	response.end(); } // 200 Okay : 정상적인 요청 

function onRequest(request, response){ 
	if(request.method == 'GET' && request.url == '/'){ 
		response.writeHead(200,{"Content-Type":"text/html"}); // 웹페이지 출력 
		fs.createReadStream("index.html").pipe(response); // 같은 디렉토리에 있는 index.html를 response 함 
		} else { 
			// file이 존재 하지않을때, 
			send404Message(response); 
		} 
	}

http.createServer(onRequest).listen(8888); 
console.log("Server Created...");​*/
app.listen(port, function(){
	console.log('Server start, Port : ' + port);
});

app.get('/', function(req, res){
	fs.readFile('index.html', function(error, data){
		if(error){
			console.log(error);
		}else{
			res.writeHead(200, {'Content-Type' : 'text/html'});
			res.end(data);
		}
	});
});
