FROM python:3.10.2-slim-bullseye
LABEL maintainer = "sprootik" \
      desc="net_proxy"

WORKDIR /app
ADD . /app
EXPOSE 4444/tcp

# install and run
RUN pip install -r requirements.txt
CMD [ "python", "./net_proxy.py"]

# healthcheck
HEALTHCHECK --interval=5s --timeout=10s --retries=3 CMD curl -sS 127.0.0.1:4444 || exit 1