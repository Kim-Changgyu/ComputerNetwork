# Python Socket 모듈을 활용한 HTTP REQUEST/RESPONSE

### 프로그램 실행법

* 서버 실행
```python
python server.py
```
* 클라이언트 실행
```python
python client.py
```

---

* 클라이언트 요청
```bash
METHOD  >> GET | POST | DELETE (외에는 Method Not Allowed 처리)
URL     >> / (URL이 중첩으로 올 경우 Not Found 처리)
VERSION >> HTTP/1.1 (상관 없음)

MESSAGE >> 서버로 전송할 메세지 (Only POST / Request Body에 담겨서 전송)
```
