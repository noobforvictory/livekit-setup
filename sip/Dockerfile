FROM golang:1.25 AS builder
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    pkg-config \
    libopus-dev \
    libopusfile-dev \
    libsoxr-dev \
    && rm -rf /var/lib/apt/lists/*WORKDIR /sip
RUN git clone https://github.com/livekit/sip.git .
RUN go install github.com/magefile/mage@v1.15.0
RUN mage build

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    libopus0 \
    libopusfile0 \
    libsoxr0 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m sip
WORKDIR /sip
COPY --from=builder /go/bin/sip /usr/local/bin/sip
RUN chmod +x /usr/local/bin/sip
USER sip
CMD ["sip", "--config=/sip/config.yaml"]
