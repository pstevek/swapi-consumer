FROM python:3.10.13-alpine3.18

LABEL maintainer="pstevek@gmail.com"

ENV PYTHONUNBUFFERED 1

# Copy dependencies accross
COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /src

WORKDIR /src
EXPOSE 8000

# Install dependecies
RUN apk update && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

ENV PATH="/py/bin:$PATH"

# Clean up
RUN rm -rf /tmp && \
    apk del .tmp-build-deps

# Add non-root user
RUN adduser --disabled-password --no-create-home ppuser
USER ppuser