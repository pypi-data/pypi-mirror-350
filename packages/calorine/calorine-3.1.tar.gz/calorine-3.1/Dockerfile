# Base image
FROM nvidia/cuda:12.2.0-devel-ubuntu22.04

# Base packages
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Gothenburg
RUN \
  apt-get update -qy && \
  apt-get upgrade -qy && \
  apt-get install -qy \
    git \
    graphviz \
    pandoc \
    python3-pip \
    zip

RUN \
  pip3 install --upgrade \
    pip \
  && \
  pip3 install --upgrade \
    coverage \
    flake8 \
    flake8-quotes \
    nbmake \
    pytest \
    setuptools_scm \
    twine==6.0.1 \
    xdoctest

# Packages needed for calorine (compare setup.py)
RUN \
  pip3 install \
    ase \
    matplotlib \
    numpy \
    pandas \
    phonopy \
    scikit-learn \
    seekpath

# Packages for building documentation
RUN \
  pip3 install --upgrade \
    sphinx \
    sphinx_autodoc_typehints \
    sphinx-rtd-theme \
    sphinx_sitemap \
    sphinxcontrib-bibtex \
    nbsphinx

# Add hiphive
RUN \
  pip3 install \
    hiphive

# Install GPUMD
RUN \
  git clone https://github.com/brucefan1983/GPUMD.git && \
  cd GPUMD && \
  # v3.9.5 commit with NEP5 as well as higher l_max
  git checkout e3e23a298 && \
  cd src && \
  make CFLAGS="-std=c++14 -O3 -arch=sm_72 -DDEBUG" -j4 && \
  mv gpumd nep /usr/local/bin/ && \
  cd ../.. && \
  rm -fr GPUMD

CMD /bin/bash
