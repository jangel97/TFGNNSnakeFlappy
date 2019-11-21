FROM python:2.7
LABEL mantainer="jamorena@essiprojects.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT ["python"]
CMD ["server.py"]