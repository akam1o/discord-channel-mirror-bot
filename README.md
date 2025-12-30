# discord-channel-mirror-bot

## Detail
Discord channel mirror bot.

## Docker
This bot is a long-running process (it keeps a connection to Discord Gateway), so running it as a container is a good fit.

### Discord bot settings (message content intent)
This bot reads message text, so you must enable "MESSAGE CONTENT INTENT" for the source bot in Discord Developer Portal.

### Run locally with Docker
```bash
docker build -t discord-channel-mirror-bot .
docker run --rm \
  -e SOURCE_CHANNEL_ID=... \
  -e SOURCE_DISCORD_BOT_TOKEN=... \
  -e TARGET_CHANNEL_ID=... \
  -e TARGET_DISCORD_BOT_TOKEN=... \
  discord-channel-mirror-bot
```

### Run with Docker Compose
1. Copy `.env.example` to `.env` and fill in values.
2. Start:
```bash
docker compose up -d
docker compose logs -f
```

## Deploy to Kubernetes
1. `k8s/deployment.yaml` uses `ghcr.io/akam1o/discord-channel-mirror-bot:latest` by default (edit if you want a different tag).
2. Fill `k8s/secret.yaml` values.
3. Apply:
```bash
kubectl apply -f k8s/secret.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deploy/discord-mirror
kubectl logs -l app=discord-mirror -f
```

## Deploy to Google Compute Engine (GCE) with a container VM
You can run the Docker image on a Container-Optimized OS VM.

1. Create a VM from a container image (example uses a free-tier-eligible machine type/region; adjust as needed):
```bash
gcloud compute instances create-with-container discord-mirror \
  --zone=us-central1-a \
  --machine-type=e2-micro \
  --boot-disk-size=30GB \
  --boot-disk-type=pd-standard \
  --container-image=ghcr.io/akam1o/discord-channel-mirror-bot:latest \
  --container-restart-policy=always \
  --container-env=SOURCE_CHANNEL_ID=... \
  --container-env=SOURCE_DISCORD_BOT_TOKEN=... \
  --container-env=TARGET_CHANNEL_ID=... \
  --container-env=TARGET_DISCORD_BOT_TOKEN=...
```

2. Check logs:
```bash
gcloud compute instances tail-serial-port-output discord-mirror --zone=us-central1-a
```
