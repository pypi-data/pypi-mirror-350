# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=too-few-public-methods
import logging
from typing import Any

import temporalio.client
from fastapi import APIRouter
from temporalloop.importer import import_from_string

from ant31box.models import AsyncResponse
from ant31box.server.exception import ResourceNotFound
from ant31box.temporal.client import tclient

router = APIRouter(prefix="/api/v1/status", tags=["antbed", "status"])

logger = logging.getLogger(__name__)


async def get_handler_from_ar(
    ar: AsyncResponse,
) -> tuple[temporalio.client.WorkflowHandle[Any, Any], Any]:
    """
    Retrieve the workflow handler and workflow object from the AsyncResponse.

    :param ar: The AsyncResponse object containing the job details.
    :return: A tuple containing the workflow handler and workflow object.
    """
    return await get_handler(ar.payload.jobs[0].uuid, ar.payload.jobs[0].uuid)


async def get_handler(
    workflow_id: str,
    workflow_name: str,
) -> tuple[temporalio.client.WorkflowHandle[Any, Any], Any]:
    """
    Retrieve the workflow handler and workflow object for the given workflow ID and name.

    :param workflow_id: The ID of the workflow.
    :param workflow_name: The name of the workflow.
    :return: A tuple containing the workflow handler and workflow object.
    """
    workflow = import_from_string(workflow_name)
    # Retrieve running workflow handler
    client = await tclient()
    return (
        client.get_workflow_handle_for(workflow_id=workflow_id, workflow=workflow.run),
        workflow,
    )


@router.post("/", response_model=AsyncResponse)
async def status(ar: AsyncResponse) -> AsyncResponse:
    """
    Retrieve the status of the workflow and update the AsyncResponse object.

    :param ar: The AsyncResponse object containing the job details.
    :return: The updated AsyncResponse object with the workflow status and result.
    """
    workflow_id = ar.payload.jobs[0].uuid
    handler, _ = await get_handler_from_ar(ar)
    describe = await handler.describe()
    j = ar.payload.jobs[0]
    if not describe.status:
        raise ResourceNotFound("Workflow not found", {"workflow_id": workflow_id})
    j.status = describe.status.name
    if describe.status == temporalio.client.WorkflowExecutionStatus.COMPLETED:
        j.result = await handler.result()
    ar.gen_signature()
    return ar
