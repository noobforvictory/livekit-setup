FROM golang:1.25 AS builder
RUN apt-get update && apt-get install -y git
WORKDIR /livekit
RUN git clone https://github.com/livekit/livekit .
RUN ./bootstrap.sh
RUN mage

FROM debian:bookworm-slim
RUN useradd -m livekit
COPY --from=builder /livekit/bin/livekit-server /usr/local/bin/livekit-server
RUN chmod +x /usr/local/bin/livekit-server
USER livekit
CMD ["livekit-server", "--dev", "--bind", "0.0.0.0"]
