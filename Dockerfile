FROM ubuntu:onbuild
LABEL authors="chetan"

ENTRYPOINT ["top", "-b"]