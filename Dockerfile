# 使用基于 Alpine 的官方 Python 镜像作为基础镜像
FROM python:3-alpine

# 安装 gcc、musl-dev 和 libffi-dev
RUN apk add --no-cache gcc musl-dev libffi-dev

# 将当前目录的内容复制到工作目录中
COPY ./app /app

# 安装依赖
RUN pip install fastapi uvicorn alibabacloud_alidns20150109 -i https://pypi.tuna.tsinghua.edu.cn/simple

# 定义环境变量
ENV ACCESS_KEY_ID=your_access_key_id
ENV ACCESS_KEY_SECRET=your_access_key_secret
ENV REDIR_RR_ID=your_redir_rr_id
ENV REDIR_RR=your_redir_rr
ENV REDIR_RR_VALUE=your_redir_rr_value
ENV SRV_RR_ID=your_srv_rr_id
ENV SRV_RR=your_srv_rr
ENV SRV_RR_VALUE=your_srv_rr_value
ENV QB_USERNAME=admin
ENV QB_PASSWORD=adminadmin
ENV QB_ADDR=127.0.0.1:8080
ENV DEFAULT_URL=https://www.baidu.com

# 设置工作目录
WORKDIR /app

# 指定容器启动时运行的命令
CMD ["uvicorn", "main:app", "--port", "8848"]