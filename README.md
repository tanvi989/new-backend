# newbackend

Multifolks backend API (FastAPI) – auth, cart, orders, products, payments.

**Production:** https://newbackend.multifolks.com

## Quick start

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and set `MONGO_URI`, `SECRET_KEY`, etc. Then:

```bash
python app.py
```

Server runs at `http://0.0.0.0:5000`. Docs: `/docs`, health: `/api/health`.

## CORS

CORS is configured to allow **all origins** (no CORS errors from any frontend or domain).

## Deploy (e.g. newbackend.multifolks.com)

- Set env vars on the server (MONGO_URI, SECRET_KEY, STRIPE_*, etc.).
- Run with: `python app.py` or use gunicorn/uvicorn behind nginx.
- Point DNS for `newbackend.multifolks.com` to the server and use HTTPS (e.g. Let’s Encrypt).
