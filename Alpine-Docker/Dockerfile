####################################################################################################
## Builder image
####################################################################################################
# Credits to Ellie (@TheSilkky) for the original system + Dockerfile
# Modifed for use with Poetry
FROM python:3.10.6-alpine3.16 AS builder

RUN apk add --no-cache \
    ca-certificates \
    build-base \
    curl \
    linux-headers

# Add Poetry locally
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip setuptools
RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="${PATH}:/root/.local/bin"

WORKDIR /Miku

COPY /pyproject.toml /Miku/
COPY /poetry.lock /Miku/


# Create dependency wheels
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
    && pip wheel --wheel-dir=/Miku/wheels -r requirements.txt

####################################################################################################
## Final image
####################################################################################################
FROM python:3.10.6-alpine3.16

RUN apk add --no-cache \
    ca-certificates \
    tini \
    bash

WORKDIR /Miku

COPY /Bot/miku.py /Miku/Bot/
COPY /Bot/Cogs/ /Miku/Bot/Cogs
COPY /Bot/miku_events_utils/ /Miku/Bot/miku_events_utils
COPY /Bot/miku_config_utils/ /Miku/Bot/miku_config_utils

# Copy dependency wheels from builder stage
COPY --from=builder /Miku/wheels /Miku/wheels
COPY --from=builder /Miku/requirements.txt /Miku/requirements.txt

COPY /Alpine-Docker/start.sh /Miku/start.sh

RUN pip install --upgrade pip setuptools wheel

# Add an unprivileged user and set directory permissions
RUN adduser --disabled-password --gecos "" miku \
    && chown -R miku:miku /Miku \
    && chmod +x /Miku/start.sh

USER miku

# Install dependencies
RUN pip install --user --no-index --find-links=/Miku/wheels -r requirements.txt

ENTRYPOINT ["/sbin/tini", "--"]

CMD ["/Miku/start.sh"]

STOPSIGNAL SIGTERM

# Image metadata
LABEL org.opencontainers.image.title="Miku"
LABEL org.opencontainers.image.description="A Multipurpose bot focused on simplicity, speed and efficiency"
LABEL org.opencontainers.image.url=""
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/No767/Miku"