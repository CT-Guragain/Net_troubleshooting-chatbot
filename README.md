# Network Troubleshooter Chatbot

An AI-powered network troubleshooting assistant built with Python and the Anthropic Claude API.

## What it does
Guides engineers through systematic network diagnosis — from basic connectivity checks (ping/tracert) down to DNS, NAT, firewall policy, and port-level troubleshooting (telnet).

## Troubleshooting Logic
Follows real enterprise diagnostic flow:
1. Ping gateway and public IP → identify loss type
2. Tracert to find which hop fails
3. Isolate DNS vs NAT issues
4. Port-level check with telnet (refused vs timeout = different problems)

## Tech Stack
- Python 3
- Anthropic Claude API (claude-sonnet-4-6)
- python-dotenv

## Setup
```bash
pip install -r requirements.txt
```
Add your API key to `.env`: