import os
import subprocess
import serverboi_utils.embeds as embed_utils
import serverboi_utils.responses as response_utils
from discord import Color
import time
import socket
import a2s
import requests

from set_constants import (
    ADDRESS,
    PORT,
    RUN_CLIENT,
    STEAM_APP_DIR,
    DOWNLOAD_CLIENT,
    RUN_CLIENT,
)

"""
Generic script to bootstrap container.

Downloads game client then starts game client

"""
WORKFLOW_NAME = "Provision-Server"
APPLICATION_ID = os.environ.get("APPLICATION_ID")
INTERACTION_TOKEN = os.environ.get("INTERACTION_TOKEN")
EXECUTION_NAME = os.environ.get("EXECUTION_NAME")


def update_workflow(stage: str):
    print(stage)

    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="🟢 running",
        stage=stage,
        color=Color.green(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)


def fail_wf(stage: str):
    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="❌ failed",
        stage=stage,
        color=Color.red(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)


def download_client():

    command = DOWNLOAD_CLIENT
    print(f"Download Client Command: {command}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    while True:
        print(process.stdout.readline().decode())
        if process.poll() == 0:
            break
        update_workflow("Downloading client")
        time.sleep(30)

    print("Finished downloading client")

    advance_sfn()


def advance_sfn():
    json = {
        "application_id": APPLICATION_ID,
        "interaction_token": INTERACTION_TOKEN,
        "execution_name": EXECUTION_NAME,
        "port": PORT,
        "game": os.environ.get("GAME"),
        "name": os.environ.get("NAME"),
        "user_id": os.environ.get("USER_ID"),
        "guild_id": os.environ.get("GUILD_ID"),
        "service": os.environ.get("SERVICE"),
        "region": os.environ.get("REGION"),
        "server_id": os.environ.get("SERVER_ID"),
    }
    requests.post("https://api.serverboi.io/bootstrap", json=json)


def start_client():
    app_location = STEAM_APP_DIR
    os.chdir(app_location)

    command = RUN_CLIENT

    print("Starting client")

    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    ping_server(ADDRESS, PORT)

    update_workflow("Client started")

    advance_sfn()


def ping_server(address, port):
    query_port = int(port)
    print(f"Checking {address}:{query_port}")
    while True:
        try:
            info = a2s.info((address, query_port))
            print(info)
            break
        except socket.timeout:
            print("timeout")
            if int(port) == query_port:
                query_port = int(port + 1)
            else:
                query_port = query_port - 1
        except Exception as error:
            raise Exception(error)


def main():
    print("Bootstraping")
    update_workflow("Starting download")
    download_client()
    update_workflow("Starting client")
    start_client()


if __name__ == "__main__":
    main()