FROM python:3.8.10

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
EXPOSE 80
COPY ./market/ .
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT [ "./docker-entrypoint.sh" ]
