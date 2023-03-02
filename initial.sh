#!/bin/bash

mkdir pgdata

docker pull postgres:alpine3.17

docker pull instrumentisto/geckodriver

docker pull python:3.10-slim

docker build -f docker/parser/Dockerfile -t parser:final .

docker network create wb_net
