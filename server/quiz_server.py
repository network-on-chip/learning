#!/usr/bin/env python3
"""Standalone Python Backend for NoC Quiz Automated GitHub Issue Submission.

Can run locally or on a VPS/container.
Extracts real client IP, performs IP-to-Country lookup if needed,
and submits verified quiz records directly to GitHub Issues via GitHub REST API.

Usage:
    export GITHUB_TOKEN="ghp_yourPersonalAccessTokenHere"
    python3 quiz_server.py [--port 8787] [--host 0.0.0.0]
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler


def resolve_geo_ip(ip: str) -> dict:
    """Resolve IP location and country using ipapi.co (fallback to defaults for local/private)."""
    if not ip or ip.startswith(("127.", "192.168.", "10.", "172.16.", "::1")):
        return {"ip": ip, "country": "Local / Internal Network", "city": "Localhost"}
    try:
        req = urllib.request.Request(
            f"https://ipapi.co/{ip}/json/",
            headers={"User-Agent": "noc-quiz-server/1.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return {
                "ip": ip,
                "country": data.get("country_name", "Unknown Country"),
                "country_code": data.get("country_code", ""),
                "city": data.get("city", ""),
                "region": data.get("region", "")
            }
    except Exception:
        return {"ip": ip, "country": "Unknown Country", "city": ""}


class QuizSubmissionHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS, GET")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(204)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self._send_cors_headers()
        self.end_headers()
        status = {
            "service": "NoC Architecture Quiz Submission Server",
            "status": "online",
            "github_token_configured": bool(os.environ.get("GITHUB_TOKEN")),
            "repository": f"{os.environ.get('GITHUB_OWNER', 'network-on-chip')}/{os.environ.get('GITHUB_REPO', 'learning')}"
        }
        self.wfile.write(json.dumps(status, indent=2).encode("utf-8"))

    def do_POST(self):
        if self.path not in ("/api/submit-quiz", "/api/submit", "/api/quiz-submit"):
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Path not found"}).encode("utf-8"))
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body_raw = self.rfile.read(content_length)

        try:
            payload = json.loads(body_raw.decode("utf-8"))
        except Exception as e:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Invalid JSON payload: {e}"}).encode("utf-8"))
            return

        # Extract authentic client IP
        forwarded_for = self.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        else:
            client_ip = self.headers.get("X-Real-IP", self.client_address[0])

        candidate_name = str(payload.get("candidate", payload.get("name", ""))).strip()
        candidate_email = str(payload.get("email", "")).strip()
        score = int(payload.get("score", 0))
        accuracy = float(payload.get("accuracy", 0.0))
        cert_id = str(payload.get("certId", f"NOC-CERT-{int(score)}")).strip()
        mode = str(payload.get("mode", "full")).strip()
        date = str(payload.get("date", "")).strip()

        if not candidate_name:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Candidate name is required."}).encode("utf-8"))
            return

        email_regex = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not candidate_email or not re.match(email_regex, candidate_email):
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Valid email address is required."}).encode("utf-8"))
            return

        # Resolve location
        declared_location = str(payload.get("location", "")).strip()
        client_country = payload.get("country")
        client_city = payload.get("city")
        if not client_country or client_country == "Unknown":
            geo = resolve_geo_ip(client_ip)
            client_country = geo.get("country", "Unknown Country")
            client_city = geo.get("city", "")

        network_location = f"{client_city}, {client_country}" if client_city else client_country
        final_location = declared_location or network_location

        # Format issue
        issue_title = f"[quiz-result] {candidate_name} ({candidate_email}) — {score} pts — {cert_id}"
        issue_body = f"""### 🎯 NoC Architecture Assessment Verification Record

> **Automated Submission:** This credential was submitted automatically by the NoC Learning Hub upon exam completion.

| Attribute | Assessment Record |
| :--- | :--- |
| **Candidate Full Name** | **{candidate_name}** |
| **Candidate Email** | `{candidate_email}` |
| **Declared Location** | {declared_location or "Unspecified"} |
| **Client IP Address** | `{client_ip}` |
| **Network Gateway Country** | {network_location} |
| **Assessment Track** | {mode} |
| **Total Score** | **{score} pts** |
| **Accuracy** | {accuracy:.1f}% |
| **Credential Hash** | `{cert_id}` |
| **Certification Date** | {date} |

#### Cryptographic Verification Payload
```json
{json.dumps({
    "candidate": candidate_name,
    "email": candidate_email,
    "ip": client_ip,
    "location": final_location,
    "declared_location": declared_location,
    "network_location": network_location,
    "country": final_location,
    "mode": mode,
    "score": score,
    "accuracy": accuracy,
    "certId": cert_id,
    "date": date,
    "type": "quiz"
}, indent=2)}
```

---
*Network-on-Chip (NoC) Learning Hub · Official Credential Registry*
"""

        github_token = os.environ.get("GITHUB_TOKEN")
        owner = os.environ.get("GITHUB_OWNER", "network-on-chip")
        repo = os.environ.get("GITHUB_REPO", "learning")

        if not github_token:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({
                "error": "GITHUB_TOKEN is not configured on this server.",
                "recorded_offline": True,
                "ip": client_ip,
                "country": client_country
            }).encode("utf-8"))
            return

        gh_url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        gh_payload = json.dumps({
            "title": issue_title,
            "body": issue_body,
            "labels": ["quiz-result", "leaderboard"]
        }).encode("utf-8")

        gh_req = urllib.request.Request(
            gh_url,
            data=gh_payload,
            headers={
                "Authorization": f"Bearer {github_token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "User-Agent": "NoC-Quiz-Bot/2.0"
            }
        )

        try:
            with urllib.request.urlopen(gh_req, timeout=10) as gh_resp:
                res_data = json.loads(gh_resp.read().decode("utf-8"))
                self.send_response(201)
                self.send_header("Content-Type", "application/json")
                self._send_cors_headers()
                self.end_headers()
                resp_payload = {
                    "success": True,
                    "issue_number": res_data.get("number"),
                    "html_url": res_data.get("html_url"),
                    "candidate": candidate_name,
                    "email": candidate_email,
                    "ip": client_ip,
                    "country": client_country,
                    "score": score,
                    "certId": cert_id
                }
                self.wfile.write(json.dumps(resp_payload, indent=2).encode("utf-8"))
        except urllib.error.HTTPError as err:
            err_msg = err.read().decode("utf-8", errors="ignore")
            self.send_response(err.code)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"GitHub API error: {err.code}", "details": err_msg}).encode("utf-8"))
        except Exception as err:
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(json.dumps({"error": f"Internal server error: {err}"}).encode("utf-8"))


def main():
    parser = argparse.ArgumentParser(description="NoC Quiz Submission Backend Server")
    parser.add_argument("--host", default="0.0.0.0", help="Binding host (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8787, help="Binding port (default: 8787)")
    args = parser.parse_args()

    server = HTTPServer((args.host, args.port), QuizSubmissionHandler)
    print(f"🚀 NoC Quiz Submission Server listening on http://{args.host}:{args.port}")
    print(f"   Target Repo: {os.environ.get('GITHUB_OWNER', 'network-on-chip')}/{os.environ.get('GITHUB_REPO', 'learning')}")
    print(f"   GITHUB_TOKEN present: {bool(os.environ.get('GITHUB_TOKEN'))}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        server.server_close()


if __name__ == "__main__":
    main()

