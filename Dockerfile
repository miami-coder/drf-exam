FROM ubuntu:latest
LABEL authors="palamar"

ENTRYPOINT ["top", "-b"]