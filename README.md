# Instruction


### Setup environment
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


### Setup VS code
CMP + SHIFT + P
Python: Select Interpreter
Введите путь к интерпретатору
./venv/bin/python3.10# fastapi_auth


### Setup server

git clone <URL>

docker build -t fastapi_auth:latest .
docker run -p 127.0.0.1:4500:4500 fastapi_auth:latest# prod-hackaton-backend
