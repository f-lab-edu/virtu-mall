FROM aohus/virtu-mall-base as development

ENV VIRTUMALL_ENV=development
WORKDIR $PYSETUP_PATH

# copy in our built poetry + venv
COPY --from=aohus/virtu-mall-base $POETRY_HOME $POETRY_HOME
COPY --from=aohus/virtu-mall-base $PYSETUP_PATH $PYSETUP_PATH

# quicker install as runtime deps are already installed
RUN poetry install

# will become mountpoint of our code
WORKDIR /usr/src/app
COPY . /usr/src/app
COPY docker/run_server.sh /usr/src/app/run_server.sh

EXPOSE 8000
CMD ["bash", "run_server.sh"]
