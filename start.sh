#!/bin/sh

set -e
cp .env.sample .env
docker-compose up -d --build