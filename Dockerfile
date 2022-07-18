FROM python:3.9-slim

ENV PROTOC_VERSION=21.2
ENV GO_VERSION=1.18.4

RUN apt-get update && \
    apt-get install -y wget git unzip ssh-client nodejs npm curl apt-transport-https ca-certificates gnupg && \
    # https://github.com/protocolbuffers/protobuf/releases/download/v21.2/protoc-21.2-linux-x86_64.zip
    wget -q https://github.com/protocolbuffers/protobuf/releases/download/v${PROTOC_VERSION}/protoc-${PROTOC_VERSION}-linux-x86_64.zip -O protoc.zip && \
    unzip protoc.zip -d /usr/local && \
    rm protoc.zip

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add - && apt-get update -y && apt-get install google-cloud-cli -y

ENV PATH="${PATH}:/usr/local/go/bin:/root/go/bin:/node_modules/.bin"

RUN wget https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go${GO_VERSION}.linux-amd64.tar.gz && \
    rm go${GO_VERSION}.linux-amd64.tar.gz

RUN go version && \
    go install github.com/square/goprotowrap/cmd/protowrap@latest && \
    go install google.golang.org/protobuf/cmd/protoc-gen-go@latest

RUN npm install -g typescript && npm install -g ts-proto

RUN curl -sL https://git.io/autotag-install | sh -s -- -b /usr/local/go/bin

COPY build.py /
