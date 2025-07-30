# ECIDA
The EcidaModule package is a Python module designed to facilitate deployment and communication between components in a distributed system. This package provides various functionalities including Kafka message handling, environment variable checking, and directory management.

## How to Use

1. ### Importing the package

    To use the EcidaModule in your Python program, first, you will need to import the EcidaModule class from the package:

    ```python
    from Ecida import EcidaModule
    ```

2. ### Create an ECiDA Module
    Define a module with this signature
    ```python
    def create_module() -> EcidaModule:
        M = EcidaModule("MODULE_NAME", "MODULE_VERSION")
        # ADD MODULE INPUTS/OUTPUTS HERE
        ...
    return M
    ```

3. ### Add inputs and outputs
    Use the following syntax for adding input and output to module. You can add as many I/O as required.
    ``` python
    # ADD STREAMING INPUT WITH 
    M.add_input("INPUT_NAME", "string")
    # ADD STREAMING OUTPUT 
    M.add_output("OUTPUT_NAME", "string")
    # ADD INPUT DIRECTORY FOR FILE USE 
    M.add_input_directory("INPUT_DIRECTORY_NAME")
    # ADD OUTPUT DIRECTORY FOR FILE USE 
    M.add_output_directory("OUTPUT_DIRECTORY_NAME")
    # ADD INPUT DIRECTORY PRELOADING FROM GIT FOR FILE USE
    M.add_input_from_git("INPUT_DIRECTORY_NAME", "GIT_REPOSITORY", "DIRECTORY/PATH/IN/GIT")
    ```


4. ## Entry Point

    Use the following boiler-plate as the entry-point to your code.

    ```python
    if __name__ == "__main__":
        M = create_module()
        M.initialize()
        main(M)
    ```

    and for the main function use the following signature:
    
    ```python
    def main(M: EcidaModule):    
        #YOUR LOGIC COMES HERE
    ```


## Example python file
An example template for the modules.
```python
from Ecida import EcidaModule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_module() -> EcidaModule:
    M = EcidaModule("MODULE_NAME", "MODULE_VERSION")
    # ADD MODULE INPUTS/OUTPUTS HERE

    return M

def main(M: EcidaModule):    
    print(f"START MODULE {M.name}:{M.version}")
    # LOGIC COMES HERE
      


if __name__ == "__main__":
    M = create_module()
    M.initialize()
    main(M)
```

### NOTES
A python file can contain no more than one one module, since the module creation happens through using create_module() function with exact same signature.