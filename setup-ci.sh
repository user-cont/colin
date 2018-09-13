#!/bin/bash

echo "yum -y install yum-plugin-copr"
yum -y install yum-plugin-copr

echo "yum copr enable -y shosca/python"
yum copr enable -y shosca/python

echo "yum -y install make gcc python36 python36-devel python36-setuptools python36-pip"
yum -y install make gcc python36 python36-devel python36-setuptools python36-pip

echo "pip3 install pytest"
pip3.6 install pytest

echo "yum copr enable -y baude/Upstream_CRIO_Family"
yum copr enable -y baude/Upstream_CRIO_Family

echo "yum -y install skopeo podman atomic ostree"
yum -y install skopeo podman atomic ostree


echo "pip3.6 install ."
pip3.6 install .
