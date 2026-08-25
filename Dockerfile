FROM python:3.12-slim
LABEL authors="shmadik"

WORKDIR /app/
COPY requirements.txt .
RUN apt update && apt-get install -y --no-install-recommends nmap && rm -rf /var/lib/apt/lists/* && pip install -r requirements.txt
COPY . .
CMD [ "python" ]
 


