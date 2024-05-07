import os
import platform
import psutil
import requests
from fastapi import FastAPI
from dotenv import dotenv_values

app = FastAPI()
config = dotenv_values(".env")


# Get Cloudflare Zones
@app.get("/cloudflare/zones")
def cloudflare_zones():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/zones", headers=headers, data=data
    )
    return response.json()


# Get Cloudflare DNS Records
@app.get("/cloudflare/dns")
def cloudflare_dns():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/zones/4755d9a7f5f0fdbf0941ff1af70c206e/dns_records",
        headers=headers,
    )
    return response.json()


# Get Cloudflare Tunnel Details
@app.get("/cloudflare/tunnel")
def cloudflare_tunnel():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        # "X-Auth-User-Service-Key": config["CLOUDFLARE_USER_SERVICE_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/accounts/"
        + config["CLOUDFLARE_TUNNEL_ID"]
        + "/tunnels",
        headers=headers,
    )
    return response.json()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/info")
def info():
    return {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "virtual_memory": psutil.virtual_memory(),
        "swap_memory": psutil.swap_memory(),
        "disk_usage": psutil.disk_usage("/"),
        "ram_usage": psutil.virtual_memory().percent,
    }
