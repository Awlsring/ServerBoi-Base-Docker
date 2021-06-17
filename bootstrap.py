import os
import subprocess
import serverboi_utils.embeds as embed_utils
import serverboi_utils.responses as response_utils
from discord import Color
import time
import a2s
import requests

'''
Generic script to bootstrap container.

Downloads game client then starts game client

'''
WORKFLOW_NAME = "Provision-Server"
application_id = os.environ.get('APPLICATION_ID')
interaction_token = os.environ.get('INTERACTION_TOKEN')
EXECUTION_NAME = os.environ.get('EXECUTION_NAME')

START = time.time()


def update_workflow(stage: str):
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

    command = os.environ.get("DOWNLOAD_CLIENT")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    while True:
        if process.poll() == 0:
            break
        print(process.stdout.readline().decode())
        update_workflow("Downloading client")
        time.sleep(30)

    advance_sfn()


def advance_sfn():
    requests.post("https://api.serverboi.io/bootstrap",
                  json={"execution_id": EXECUTION_NAME})


def start_client():
    app_location = os.environ.get("STEAM_APP_DIR")
    os.chdir(app_location)

    command = os.environ.get("RUN_CLIENT")

    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)

    while True:
        if process.poll() == 0:
            break
        print(process.stdout.readline().decode())
        update_workflow("Starting client")
        time.sleep(5)

    advance_sfn()


def ping_client():
    address = os.environ.get("ADDRESS")
    port = int(os.environ.get("PORT"))

    try:
        info = a2s.info((address, port))
        print(info)
    except Exception as error:
        raise error


def main():
    print("Bootstraping")
    update_workflow("Starting download")
    download_client()
    start_client()
    # ping_client()
