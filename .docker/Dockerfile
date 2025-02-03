# Docker complaines if FROM does not resolve to a valid image. Hence the defaults.
ARG UBUNTU_VERSION=22.04
ARG UV_VERSION=0.5.15
ARG SPARK_VERSION=3.5.4

# Get Spark
FROM spark:${SPARK_VERSION}-scala2.12-java17-python3-r-ubuntu AS spark
USER root
RUN mkdir -p /tmp \
  && chmod 777 /tmp \
  && mv /opt/spark// /tmp/spark \
  && mv /opt/java/openjdk /tmp/java

# Get uv
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv

# Base image
FROM mcr.microsoft.com/devcontainers/base:ubuntu-${UBUNTU_VERSION}

# Install System Dependencies
RUN apt-get update \
  && apt-get install -y \
  git \
  curl \
  build-essential \
  # gnupg2 allows you to sign git commits with GPG
  gnupg2 \
  gcc \
  python3-dev \
  protobuf-compiler \
  && rm -rf /var/lib/apt/lists/* \
  && apt-get clean


# Copy Spark
ENV JAVA_HOME=/opt/java/openjdk
ENV SPARK_HOME=/opt/spark
COPY --from=spark /tmp/spark ${SPARK_HOME}
COPY --from=spark /tmp/java ${JAVA_HOME}
ENV PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$PATH

# Copy uv
COPY --from=uv /uv /bin
COPY --from=uv /uvx /bin
ENV PATH=/bin:$PATH

# Change to non-root user
ENV USER=vscode
ENV HOME=/home/$USER
ENV UV_PROJECT_ENVIRONMENT=$HOME/.venv
