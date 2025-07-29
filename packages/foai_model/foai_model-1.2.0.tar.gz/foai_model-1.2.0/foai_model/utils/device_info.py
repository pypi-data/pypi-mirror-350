import torch
from foai_model.logger import logger


def log_device_info():
    if torch.cuda.is_available():
        num_devices = torch.cuda.device_count()
        logger.info("CUDA is available. Found %d GPU(s).", num_devices)
        for i in range(num_devices):
            logger.info("GPU %d: %s", i, torch.cuda.get_device_name(i))
    else:
        logger.warning("CUDA not available. Using CPU.")
