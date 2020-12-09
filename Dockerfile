FROM python:2.7
LABEL authors="jangel97,eduardfores"
COPY . /app
WORKDIR /app
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir
COPY . /app
RUN useradd -ms /bin/bash flappy && \
    usermod -aG flappy flappy && \
    chown -R flappy:flappy /app
USER flappy
ENTRYPOINT ["python"]
CMD ["server.py"]
