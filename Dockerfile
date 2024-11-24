FROM python:3-alpine

WORKDIR /app/polls
COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .
RUN chmod +x ./entrypoint.sh

EXPOSE 8000
CMD [ "./entrypoint.sh" ]
