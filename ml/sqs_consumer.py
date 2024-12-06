import boto3
from message_processor import (
    SignalHandler,
    logger,
    RAW_MOUNT_POINT,
    process_message
)

QUEUE_NAME = "your-queue-name"
DLQ_NAME = "your-dlq-name"


def message_loop():

    signal_handler = SignalHandler()
    sqs = boto3.resource("sqs")

    sqs_queue = sqs.get_queue_by_name(QueueName=QUEUE_NAME)
    dl_queue = sqs.get_queue_by_name(QueueName=DLQ_NAME)

    while not signal_handler.received_signal:
        messages = sqs_queue.receive_messages(MaxNumberOfMessages=1, WaitTimeSeconds=60)
        for message in messages:
            try:
                process_message(message.body)
                logger.info(f"Message {message} processed!")
                message.delete()
                logger.info(f"Message {message} deleted!")
            except Exception as e:
                logger.error(
                    f"Exception while processing message: {repr(e)} for message : '{message}'"
                )
                # put into dead letter queue and maybe do something later?
                dl_queue.send_message(MessageBody=message.body)         #"https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs/client/send_message.html"
                logger.info(f"Message {message} got sent to dlq")
                message.delete()
                logger.info(f"Message {message} deleted!")
                continue
    pass


if __name__ == "__main__":
    message_loop()
