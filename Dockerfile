FROM python:3.10-alpine

WORKDIR /prod-hackaton-backend

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD python run.py