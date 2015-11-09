FROM fedora:21

MAINTAINER "Jiao Lin <jiao.lin@gmail.com>"

RUN yum install -y deltarpm
RUN yum install -y git cmake make gcc-c++ python python-devel rpm-build
RUN yum install -y numpy

RUN rpmbuild --rebuild ${PARENT_GITHUB_URL}/releases/download/v${PARENT_VERSION}/${PARENT_PY_PKG}-${PARENT_VERSION}-${PARENT_RELEASE}.src.rpm
RUN rpm -i ~/rpmbuild/RPMS/x86_64/${PARENT_PY_PKG}-${PARENT_VERSION}-${PARENT_RELEASE}.x86_64.rpm
