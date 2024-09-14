FROM --platform=linux/amd64 ubuntu:24.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pwntools git gdb python3-ropgadget netcat-openbsd curl wget gcc file unzip zip

COPY pwntools-fake-term.sh /opt/pwntools-fake-term.sh
RUN chmod +x /opt/pwntools-fake-term.sh

WORKDIR /root