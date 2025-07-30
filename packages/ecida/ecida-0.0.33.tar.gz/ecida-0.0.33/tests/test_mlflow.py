# from ecidaModule import EcidaModule
# Get the absolute path of the package-ecida directory
from src.Ecida import EcidaModule

import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_module() -> EcidaModule:
    M = EcidaModule("mlflow-test", "v1")
    logger.info("test logger")
    return M


def main():
    M = create_module()
    M.initialize()

    M.log_params(alpha=0.01, gamma=0.2)

    for i in range(0, 25):
        M.log_metric("accuracy", random.random())
        M.log_metric("precision", random.random())


if __name__ == "__main__":
    main()
