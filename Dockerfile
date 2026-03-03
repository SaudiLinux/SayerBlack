FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN apt update && apt install -y nmap
CMD ["python", "main.py"]
