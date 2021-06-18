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
application_id = os.environ.get("APPLICATION_ID")
interaction_token = os.environ.get("INTERACTION_TOKEN")
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
    response_utils.edit_response(application_id, interaction_token, data)


def fail_wf(stage: str):
    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="❌ failed",
        stage=stage,
        color=Color.red(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(application_id, interaction_token, data)


def download_client():

    command = DOWNLOAD_CLIENT
    print(f"Download Client Command: {command}")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    while True:
        if process.poll() == 0:
            break
        print(process.stdout.readline().decode())
        update_workflow("Downloading client")
        time.sleep(30)

    print("Finished downloading client")

    advance_sfn()


def advance_sfn():
    requests.post(
        "https://api.serverboi.io/bootstrap", json={"execution_id": EXECUTION_NAME}
    )


def start_client():
    app_location = STEAM_APP_DIR
    os.chdir(app_location)

    command = RUN_CLIENT

    print("Starting client")

    subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    ping_server()

    update_workflow("Client started")

    advance_sfn()


def ping_server():
    process = subprocess.Popen(
        "python3 /opt/serverboi/scripts/ping.py", stdout=subprocess.PIPE, shell=True
    )
    while True:
        if process.poll() == 0:
            break
        print("No response, waiting 10 seconds.")
        time.sleep(10)


def main():
    print("Bootstraping")
    update_workflow("Starting download")
    download_client()
    update_workflow("Starting client")
    start_client()


if __name__ == "__main__":
    main()
