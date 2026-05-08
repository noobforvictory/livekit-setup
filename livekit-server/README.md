# LiveKit Server

Build the image:

```bash
docker build --network=host -t livekit-server-local .
```

Check it built correctly:

```bash
docker run --rm livekit-server-local livekit-server --version
```

Run the server:

```bash
  docker run --rm --network=host livekit-server-local
```
