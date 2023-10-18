FROM python:3.10.13-alpine3.18

LABEL maintainer="pstevek@gmail.com"

ENV PYTHONUNBUFFERED 1

# Copy dependencies accross
COPY ./requirements.txt /tmp/requirements.txt
COPY ./src /src

WORKDIR /src
EXPOSE 8000

# Install dependecies
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

ENV PATH="/py/bin:$PATH"

# Clean up
RUN rm -rf /tmp

# Add non-root user
RUN adduser --disabled-password --no-create-home postpayuser
USER postpayuser