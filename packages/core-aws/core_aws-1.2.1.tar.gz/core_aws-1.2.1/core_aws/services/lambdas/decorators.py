# -*- coding: utf-8 -*-

from __future__ import annotations

import json
from functools import wraps
from logging import Logger
from typing import Callable, Dict, List, Optional

from core_aws.services.lambdas.events.base import EventRecord
from core_aws.services.sqs.client import SqsClient
from core_aws.typing.lambda_context import LambdaContext


def process_sqs_batch(
        message_handler: Callable[[EventRecord], ...], logger: Logger,
        post_process_fcn: Optional[Callable] = None):

    """
    It provides a mechanism to process incoming messages. It implements partial batch responses
    to report the messages that failed. Feature "Report batch item failures" MUST be
    activated in the lambda trigger...

    More information...
      * https://docs.aws.amazon.com/lambda/latest/dg/with-sqs.html#services-sqs-batchfailurereporting
      * https://repost.aws/knowledge-center/lambda-sqs-report-batch-item-failures

    ****************************************************************************************
    How to use...
    ****************************************************************************************

    .. code-block:: python

        def message_handler(record: EventRecord):
            \""" Here the code that process each message \"""

        def post_process_fcn():
            \""" Here the code to execute after the handler \"""

        @process_batch(message_handler=message_handler, logger=logger, post_process_fcn=post_process_fcn)
        def handler(event: Dict, context):
            \""" A body is not required, but the code added here will be executed at the beginning \"""
    ..

    :param message_handler: Function's reference which process each message.
    :param logger: Object for logging.

    :param post_process_fcn:
        Function to be called after processing the messages. For
        clean/release purposes for instance.
    """

    def decorator(handler: Callable):
        @wraps(handler)
        def execute(event: Dict, context: LambdaContext) -> Dict:
            logger.info("Starting the execution of handler function...")
            handler(event, context)

            logger.info("Processing the incoming event and the records within it...")
            batch_item_failures: List[Dict[str, str]] = []

            for record in event.get("Records", []):
                record = EventRecord.from_dict(record)
                message_id = record.message_id if issubclass(record.__class__, (EventRecord,)) else None

                try:
                    logger.info(f"Processing message [{message_id}]...")
                    message_handler(record)
                    logger.info(f"Message [{message_id}] processed successfully!")

                except Exception as error:
                    batch_item_failures.append({"itemIdentifier": message_id})
                    logger.error({"MessageId": message_id, "error": str(error)})

            if post_process_fcn:
                logger.info("Processing post process function...")
                post_process_fcn()

            logger.info("Execution Done!")
            return {"batchItemFailures": batch_item_failures}

        return execute

    return decorator


def process_sqs_messages(
        sqs_client: SqsClient, sqs_queue_url: str, function: Callable[[EventRecord], ...],
        logger: Logger, post_process_fnc: Optional[Callable] = None):

    """
    Its purpose is to provide the mechanism for message processing and safe error handling
    in the execution of a Lambda Function (that reads from SQS), avoid retries
    of messages that were processed successfully, and avoid sending them to
    a Dead Letter queue if it is configured...

    .. warning::

        **DEPRECATED** in flavor of process_sqs_batch...

    ****************************************************************************************
    How to use...
    ****************************************************************************************

    .. code-block:: python

        def record_handler(record: EventRecord):
            "Here the code to process each message"
            pass

        def post_process_fnc():
            "Here the code to be precessed after the handler"
            pass

        @process_sqs_messages(
            sqs_client=sqs_client, sqs_queue_url="SomeQueueUrl", function=record_handler,
            logger=logger, post_process_fnc=post_process_fnc)
        def handler(event: Dict, context):
            \"""
            A body is not required, but the code you put in the function
            body will be executed at the beginning...
            \"""
    ..

    :param sqs_client: Client will be used to delete messages.
    :param sqs_queue_url: URL for the queue.
    :param function: Function's reference which process each message.
    :param logger: Object for logging.

    :param post_process_fnc:
        Function to be called after processing the messages. For
        clean/release purposes for instance.
    """

    def decorator(fcn: Callable):
        @wraps(fcn)
        def execute(event: Dict, context: LambdaContext):
            logger.info("Starting execution...")
            logger.info("Executing decorated function (handler) before processing the records...")
            fcn(event, context)

            logger.info("Processing records/messages from the event...")
            success_entries, failed_records = [], []

            for record in event.get("Records", []):
                message_id, receipt_handle = record["messageId"], record["receiptHandle"]
                logger.info(f"Processing message [{message_id}]...")

                try:
                    function(record)
                    success_entries.append({"Id": message_id, "ReceiptHandle": receipt_handle})
                    logger.info(f"Message [{message_id}] processed!")

                except Exception as error:
                    error_metadata = {
                        "Id": message_id,
                        "ReceiptHandle": receipt_handle,
                        "error": str(error)
                    }

                    failed_records.append(error_metadata)
                    logger.error(error_metadata)

            if success_entries:
                sqs_client.delete_message_batch(
                    queue_url=sqs_queue_url,
                    entries=success_entries
                )

            if post_process_fnc:
                post_process_fnc()

            if failed_records:
                logger.warning("Some records failed! Below, you will find the errors reports...")

                for metadata in failed_records:
                    logger.info({
                        "MessageId": metadata["Id"],
                        "ReceiptHandle": metadata["ReceiptHandle"],
                        "Error": metadata["error"]
                    })

                raise Exception(json.dumps([msg["Id"] for msg in failed_records]))

            logger.info("Execution Done!")

        return execute

    return decorator
