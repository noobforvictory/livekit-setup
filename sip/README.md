# LiveKit SIP

Run these from this directory unless the command says otherwise.

## Start Redis

```bash
docker run --rm -d --name livekit-redis --network=host redis:7-alpine
```

If you already have Redis running on `localhost:6379`, skip this.

## Start LiveKit Server

```bash
cd ../livekit-server
docker build --network=host -t livekit-server-local .
docker run --rm -d --name livekit-server-dev --network=host livekit-server-local
```

## Build And Run SIP

```bash
cd ../sip
docker build --network=host -t livekit-sip-local .
docker run --rm -d --name livekit-sip-dev --network=host -v "$PWD/config.yaml:/sip/config.yaml:ro" livekit-sip-local
```

## Logs

```bash
docker logs livekit-server-dev --tail 100
docker logs livekit-sip-dev --tail 100
docker logs -f livekit-sip-dev
```

## Stop

```bash
docker stop livekit-sip-dev livekit-server-dev livekit-redis
```
