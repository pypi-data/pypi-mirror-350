# from ecidaModule import EcidaModule
# Get the absolute path of the package-ecida directory
from package_ecida.src.Ecida import EcidaModule

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Inp = "inppppp"


def create_module() -> EcidaModule:
    M = EcidaModule("producer", "v2")
    M.add_output("message", "string")
    M.add_input(Inp, "strings")
    M.enable_large_messages()
    print(Inp)
    logger.info("test logger")
    return M


def main():
    M = create_module()
    M.initialize()

    i = 1
    while True:
        msg = "#" + str(i)
        M.push("message", msg)
        i += 1
        logging.info("Send message:\t" + msg)
        time.sleep(5)


if __name__ == "__main__":
    main()
