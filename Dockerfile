FROM python:3.12

WORKDIR /bot 
COPY . .

CMD ["python", "index.py"]
