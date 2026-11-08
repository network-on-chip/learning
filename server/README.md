# 🚀 NoC Quiz Automated GitHub Issue Submission Server

This directory contains the automated backend bridge for recording Network-on-Chip (NoC) architecture quiz certifications to GitHub Issues.

## Why a Backend Bridge?
1. **Security (No Token Leakage):** Browser JavaScript cannot safely hold a GitHub Personal Access Token (PAT). Secret scanning on GitHub immediately revokes tokens committed or transmitted to public repositories.
2. **Authentic IP & Country Recording:** Cloudflare Workers and reverse proxies extract the authentic client IP address (`cf-connecting-ip` / `x-forwarded-for`) and country code (`cf-ipcountry`) directly at the network edge, preventing client-side spoofing.
3. **Automated Submission:** When a candidate completes the quiz, the result is submitted automatically in the background without requiring the candidate to have a GitHub account or manually open an issue tab.

---

## Option 1: Cloudflare Worker (Recommended · Free · Serverless)

Cloudflare Workers provides 100,000 free requests per day, runs on global edge datacenters with sub-10ms response times, and automatically attaches verified IP and Country headers.

### Deployment Steps:
1. Ensure Node.js is installed.
2. Navigate to this directory:
   ```bash
   cd share/learning/server
   ```
3. Set your GitHub Personal Access Token as a secret:
   ```bash
   npx wrangler secret put GITHUB_TOKEN
   # Paste your fine-grained or classic PAT with 'Issues: Read & Write' permission on network-on-chip/learning
   ```
4. Deploy the worker:
   ```bash
   npx wrangler deploy
   ```
5. Note the deployed URL (e.g. `https://noc-quiz-api.<your-subdomain>.workers.dev`).
6. Update `endpoint` in `share/learning/docs/config/site.json`:
   ```json
   "results": {
     "endpoint": "https://noc-quiz-api.<your-subdomain>.workers.dev/api/submit-quiz"
   }
   ```

---

## Option 2: Standalone Python Server (Local / VPS / Container)

If you prefer self-hosting on a Linux VPS, Docker container, or testing locally:

```bash
cd share/learning/server

# Set environment variables
export GITHUB_TOKEN="ghp_yourPersonalAccessTokenHere"
export GITHUB_OWNER="network-on-chip"
export GITHUB_REPO="learning"

# Run the server (default port: 8787)
python3 quiz_server.py --port 8787
```

To run with systemd or in the background:
```bash
nohup python3 quiz_server.py --host 0.0.0.0 --port 8787 > quiz_server.log 2>&1 &
```

---

## API Contract

### `POST /api/submit-quiz`

#### Request Payload (JSON):
```json
{
  "candidate": "Dr. Ada Lovelace",
  "email": "ada@example.com",
  "ip": "103.18.0.19",
  "country": "Malaysia (MY)",
  "location": "Kuala Lumpur",
  "mode": "full",
  "score": 1200,
  "accuracy": 100,
  "certId": "NOC-CERT-2026-F38A12",
  "date": "2026-11-08"
}
```

#### Response (JSON, HTTP 201 Created):
```json
{
  "success": true,
  "issue_number": 42,
  "html_url": "https://github.com/network-on-chip/learning/issues/42",
  "candidate": "Dr. Ada Lovelace",
  "email": "ada@example.com",
  "ip": "103.18.0.19",
  "country": "MY",
  "score": 1200,
  "certId": "NOC-CERT-2026-F38A12"
}
```
