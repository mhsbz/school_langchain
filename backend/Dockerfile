FROM python:3.10-slim

WORKDIR /app

# 创建日志目录并设置权限
RUN mkdir -p /app/logs \
    && chmod 777 /app/logs

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p /app/emd_model



# 复制应用代码
COPY ./app /app/app
COPY ./data /app/data


# 设置环境变量
ENV PYTHONPATH=/app

# 暴露端口
EXPOSE 3000

# 启动应用
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]

## uvicorn app.main:app --host 0.0.0.0 --port 8001