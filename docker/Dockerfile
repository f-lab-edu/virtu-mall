FROM aohus/virtu-mall-base:latest

COPY . /usr/src/app
COPY docker/run_server.sh /usr/src/app/run_server.sh

EXPOSE 8000

CMD ["bash", "run_server.sh"]
