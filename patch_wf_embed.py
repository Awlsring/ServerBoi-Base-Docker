import os
import click
import time
from discord import Color
import serverboi_utils.embeds as embed_utils
import serverboi_utils.responses as response_utils

WORKFLOW_NAME = "Provision-Server"
EXECUTION_NAME = os.environ.get("EXECUTION_NAME")

APPLICATION_ID = os.environ.get("APPLICATION_ID")
INTERACTION_TOKEN = os.environ.get("INTERACTION_TOKEN")


@click.group()
def cli():
    pass


@cli.command()
@click.option("-s", "--stage", "stage", required=True, type=str)
def change_stage(stage: str):
    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="🟢 running",
        stage=stage,
        color=Color.green(),
    )

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)


@cli.command()
@click.option("-s", "--start", "start", required=True, type=str)
@click.option("-e", "--end", "end", required=True, type=str)
def finish_wf(start: int, end: int):
    embed = embed_utils.form_workflow_embed(
        workflow_name=WORKFLOW_NAME,
        workflow_description=f"Workflow ID: {EXECUTION_NAME}",
        status="✔️ finished",
        stage="Complete",
        color=Color.dark_green(),
    )

    total = int(start) - int(end)
    time = time.strftime("%M:%S", time.gmtime(total))

    embed.add_field(name="Run Time", value=f"{time} minutes", inline=False)

    data = response_utils.form_response_data(embeds=[embed])
    response_utils.edit_response(APPLICATION_ID, INTERACTION_TOKEN, data)


@cli.command()
@click.option("-s", "--stage", "stage", required=True, type=str)
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


if __name__ == "__main__":
    cli()