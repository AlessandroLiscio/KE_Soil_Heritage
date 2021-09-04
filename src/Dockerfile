FROM python:3.9.7-bullseye 

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN python main.py

# CMD ["python3", "python"]
