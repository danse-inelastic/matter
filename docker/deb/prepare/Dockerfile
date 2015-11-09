FROM ubuntu:14.04

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

RUN apt-get update
RUN apt-get install -y git build-essential
RUN apt-get install -y cmake
RUN apt-get install -y python python-dev
RUN apt-get install -y python-numpy


RUN apt-get install wget
RUN wget ${PARENT_GITHUB_URL}/releases/download/v${PARENT_VERSION}/${PARENT_PY_PKG}-${PARENT_VERSION}-${PARENT_RELEASE}.x86_64.deb
RUN dpkg -i ${PARENT_PY_PKG}-${PARENT_VERSION}-${PARENT_RELEASE}.x86_64.deb
