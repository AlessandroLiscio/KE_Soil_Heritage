FROM python:3.9.7-bullseye 
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
CMD ["python3"]
RUN python main.py
