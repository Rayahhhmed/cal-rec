FROM python:alpine

COPY requirements.txt .
RUN pip3 install -r requirements.txt 

COPY . .
EXPOSE 5000 

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]