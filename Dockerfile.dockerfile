FROM python:3.9-slim
LABEL "language"="python"
LABEL "framework"="fastapi"

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 複製 main.py 到 /home/node
RUN mkdir -p /home/node && cp main.py /home/node/main.py

EXPOSE 8080

# 從 /home/node 讀取 main.py 並運行
CMD ["uvicorn", "/home/node/main:app", "--host", "0.0.0.0", "--port", "8080"]
