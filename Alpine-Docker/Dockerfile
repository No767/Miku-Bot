####################################################################################################
## Builder image
####################################################################################################
FROM python:3.10.7-alpine3.16 AS builder

RUN apk add --no-cache \
    ca-certificates \
    build-base \
    curl \
    linux-headers

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Miku

COPY /pyproject.toml /Miku/
COPY /poetry.lock /Miku/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip wheel --wheel-dir=/Miku/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10.7-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Miku

COPY /Bot/miku.py /Miku/Bot/
COPY /Bot/Cogs/ /Miku/Bot/Cogs
COPY /Bot/miku_events_utils/ /Miku/Bot/miku_events_utils
COPY /Bot/miku_config_utils/ /Miku/Bot/miku_config_utils
COPY /Bot/genshin_wish_sim_utils/ /Miku/Bot/genshin_wish_sim_utils
COPY /Alpine-Docker/start.sh /Miku/start.sh

COPY --from=builder /Miku/wheels /Miku/wheels
COPY --from=builder /Miku/requirements.txt /Miku/requirements.txt

RUN pip install --upgrade pip setuptools wheel

RUN adduser --disabled-password --gecos "" miku \
    && chown -R miku:miku /Miku \
    && chmod +x /Miku/start.sh

USER miku

RUN pip install --user --no-index --find-links=/Miku/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Miku/start.sh"]

STOPSIGNAL SIGTERM

LABEL org.opencontainers.image.title="Miku"
LABEL org.opencontainers.image.description="A Multipurpose bot focused on simplicity, speed and efficiency"
LABEL org.opencontainers.image.url=""
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Miku"