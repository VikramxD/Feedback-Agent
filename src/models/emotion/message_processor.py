from subprocess import Popen
import logging
import os
import psutil
from signal import signal, SIGINT, SIGTERM
import sys
import time

process = psutil.Process()
logging.basicConfig(
    filename="./message_processor.log",
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)
# add console into it
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("Starting Message Processor - importing models")
logger.info(f"Memory Usage RSS (bytes) Starting : {process.memory_info().rss}")
logger.info(f"Memory Usage VMS (bytes) Starting : {process.memory_info().vms}")


from emo.emo import voice_text_emo_er

logger.info("All Models Were imported and loaded...")
logger.info(
    f"Memory Usage RSS (bytes) Post Loading Models : {process.memory_info().rss}"
)
logger.info(
    f"Memory Usage VMS (bytes) Post Loading Models : {process.memory_info().vms}"
)
# This here, shows that the VMS moved to 11 GB while RSS is around 1GB

# ZSH path
ZSH = "/usr/bin/zsh"

# mount point for the s3 file system for audio upload
RAW_MOUNT_POINT = "../apis/data/user_data/bucket/raw/"

# mount point for the s3 file system foit's going to show changes in gitignore butr audio upload
USER_MOUNT_POINT = "../apis/data/user_data/bucket/users/"

# queue where the messages to be sent
QUEUE_NAME = "your-queue-name"


class SignalHandler:
    def __init__(self):
        self.received_signal = False
        signal(SIGINT, self._signal_handler)
        signal(SIGTERM, self._signal_handler)

    def _signal_handler(self, got_this_signal, frame):
        logger.info(f"handling signal {got_this_signal}, exiting gracefully")
        self.received_signal = True


def get_destination_directory(message_body):
    last_name = message_body.split("/")[-1]
    last_name = last_name[0 : last_name.rindex(".")]
    lbi = last_name.index("(") + 1
    rbi = last_name.index(")")
    user_id = last_name[lbi:rbi]
    rbi = message_body.rfind("/")
    time_stamp = message_body[0:rbi]
    destination_dir = USER_MOUNT_POINT + user_id + "/" + time_stamp
    return destination_dir


def run_voice_2_text(src_file, tmp_dir):
    logger.info(f"Spawned process for audio processing : {src_file} @ {tmp_dir}")
    p = Popen([ZSH, "./voice-2-text.sh", str(src_file), str(tmp_dir)])
    logger.info("Waiting for audio processing to finish!")
    p.wait()
    logger.info("Process finished")
    pass


def run_finalize(tmp_dir, destination_dir):
    logger.info(f"Spawned process for copying all {tmp_dir} at {destination_dir}")
    p = Popen([ZSH, "./finalize.sh", str(tmp_dir), str(destination_dir)])
    logger.info("Waiting for it to finish!")
    p.wait()
    logger.info("Process finished")
    pass

def process_message(message_body):
    logger.info(f"processing message: {message_body}")
    tmp_dir = temp_dir()
    logger.info(f"created temporary directory {tmp_dir} for {message_body}")
    input_file = RAW_MOUNT_POINT + message_body
    logger.info(f"Input audio file is : {input_file}")
    run_voice_2_text(input_file, tmp_dir)
    logger.info("Input is processed to produce wav...now ML models will run...")
    voice_text_emo_er(tmp_dir)
    logger.info("Done running ML Models")
    # now finalize it by copying back to destination
    destination_dir = get_destination_directory(message_body)
    logger.info(f"Results would be copied to : {destination_dir}")
    run_finalize(tmp_dir, destination_dir)
    logger.info("Results copied, tmp directory removed!")
    logger.info(
        f"Memory Usage RSS (bytes) Post Processing Message : {process.memory_info().rss}"
    )
    logger.info(
        f"Memory Usage VMS (bytes) Post Processing Message : {process.memory_info().vms}"
    )
    pass


def temp_dir():
    ts = str(round(time.time() * 1000))
    temp_dir_name = "/tmp/" + ts
    os.makedirs(temp_dir_name)
    return temp_dir_name


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a message argument")
        sys.exit(-1) 

    process_message(sys.argv[1])
