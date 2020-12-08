FROM python:2.7
LABEL mantainer="jamorena@essiprojects.com"
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY . /app
ENTRYPOINT ["python"]
CMD ["server.py"]
