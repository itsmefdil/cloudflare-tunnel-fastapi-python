import os
import platform
import psutil
import requests
import json
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
        "https://api.cloudflare.com/client/v4/zones",
        headers=headers,
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


# Get Cloudflare Tunnel Configurations
@app.get("/cloudflare/tunnel/configurations")
def cloudflare_tunnel_configurations():
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
        + config["CLOUDFLARE_TUNNEL_ID"]
        + "/configurations",
        headers=headers,
    )

    data = json.loads(response.text)
    data = data["result"]["config"]["ingress"]

    return data


# Get Cloudflare Tunnel Configurations
@app.get("/cloudflare/tunnel/configurations1")
def cloudflare_tunnel_configurations():
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
        + config["CLOUDFLARE_TUNNEL_ID"]
        + "/configurations",
        headers=headers,
    )

    return response.json()


# Put Cloudflare Tunnel Configurations
@app.put("/cloudflare/tunnel/configurations")
def post_cf_tunnel_hostnames(
    name: str,
    service: str,
    path: str = None,
):
    url = (
        "https://api.cloudflare.com/client/v4/accounts/"
        + config["CLOUDFLARE_TUNNEL_ACCOUNT_ID"]
        + "/cfd_tunnel/"
        + config["CLOUDFLARE_TUNNEL_ID"]
        + "/configurations"
    )
    headers = {
        "X-Auth-Email": config["CLOUDFLARE_EMAIL"],
        "X-Auth-Key": config["CLOUDFLARE_API_KEY"],
        "Authorization Bearer": config["CLOUDFLARE_TOKEN"],
        "Content-Type": "application/json",
    }

    old_data = json.loads(response.text)
    old_data = data["result"]["config"]["ingress"]
    old_data = old_data[:-1]

    data = {
        "config": {
            "warp-routing": {
                "enabled": True,
            },
            "ingress": [
                *old_data,
                {
                    "hostname": name,
                    "service": service,
                    "path": path,
                    "originRequest": {
                        "connectTimeout": 10,
                    },
                },
                {"service": "http_status:404"},
            ],
        }
    }

    response = requests.put(url, headers=headers, json=data)

    if response.status_code == 200:
        print("Configuration updated successfully.")
    else:
        print("Error updating configuration:", response.text)
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
