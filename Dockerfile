FROM python:3.11.7
WORKDIR /temp1
ADD . /temp1
RUN pip install -r requirements.txt
EXPOSE 8080
CMD [ "python", "app.py" ]


