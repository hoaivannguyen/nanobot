# Deploy Bridge to Railway via CLI

## Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

## Step 2: Login to Railway
```bash
railway login
```
This will open a browser for authentication.

## Step 3: Navigate to bridge directory
```bash
cd bridge
```

## Step 4: Initialize Railway project
```bash
railway init
```
- This creates a new Railway project
- Name it something like "nanobot-whatsapp-bridge"

## Step 5: Deploy
```bash
railway up
```
This will:
- Upload your bridge code
- Install dependencies (npm install)
- Build TypeScript (npm run build)
- Start the server (npm start)

## Step 6: Generate public domain
```bash
railway domain
```
Copy the generated URL (e.g., `bridge-production-xxxx.up.railway.app`)

## Step 7: Check logs
```bash
railway logs
```
You should see:
```
🐈 nanobot WhatsApp Bridge
========================

🌉 Bridge server listening on ws://0.0.0.0:XXXX
```

## Important Notes:
- The bridge will run on Railway's assigned PORT
- You'll need to scan the QR code again on Railway (check logs for QR)
- Use `wss://` (not `ws://`) for the bridge URL when connecting from Python
