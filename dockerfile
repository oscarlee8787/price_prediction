FROM python:3.10.6-buster

COPY /price_prediction /price_prediction
COPY /requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

CMD uvicorn price_prediction.api.veryfast:app --host 0.0.0.0
