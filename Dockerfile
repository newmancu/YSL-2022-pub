FROM python:3.8.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80
COPY ./market/ ./market/
RUN chmod +x ./market/docker-entrypoint.sh
ENTRYPOINT [ "./market/docker-entrypoint.sh" ]
