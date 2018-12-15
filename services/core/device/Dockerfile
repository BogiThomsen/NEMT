FROM python:3.6-alpine
COPY ./app /code
WORKDIR /code
RUN pip3 install -r requirements.txt
CMD ["python3", "-u", "app/main.py"]
