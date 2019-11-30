FROM python:3

ADD ./ /srv/
ENTRYPOINT [ "ls -la /srv/" ]