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
        "https://api.cloudflare.com/client/v4/zones/"
        + config["CLOUDFLARE_ZONE_ID"]
        + "/dns_records",
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
        + config["CLOUDFLARE_TUNNEL_ACCOUNT_ID"]
        + "/cfd_tunnel/"
        + config["CLOUDFLARE_TUNNEL_ID"],
        headers=headers,
    )
    return response.json()


# Get CF List All Tunnels
@app.get("/cloudflare/tunnels/all")
def get_cf_tunnels_all():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/accounts/"
        + config["CLOUDFLARE_TUNNEL_ACCOUNT_ID"]
        + "/tunnels",
        headers=headers,
    )
    return response.json()


# Get CF List Tunnels Connections
@app.get("/cloudflare/tunnels/connections")
def get_cf_tunnels_connections():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/accounts/"
        + config["CLOUDFLARE_TUNNEL_ACCOUNT_ID"]
        + "/cfd_tunnel/b1c2610f-ca96-4fcc-8b71-b71b6adcb231/connections",
        headers=headers,
    )
    return response.json()


# Get CF Tunnel Warp
@app.get("/cloudflare/tunnel/warp")
def get_cf_tunnel_wrap():
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_API_KEY"],
        "Content-Type": "application/json",
    }
    response = requests.get(
        "https://api.cloudflare.com/client/v4/accounts/"
        + config["CLOUDFLARE_TUNNEL_ACCOUNT_ID"]
        + "/warp_connector",
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
