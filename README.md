# Microservices with Docker Compose

This repository contains a set of microservices Dockerized using Docker Compose for easy deployment and management. Each service is designed to perform specific tasks, and they interact with each other through RabbitMQ message broker.

# Services

## RabbitMQ Service

- **Image**: rabbitmq:3-management
- **Description**: Provides a message broker for inter-service communication.
- **Healthcheck**: Utilizes RabbitMQ's ping diagnostic for health monitoring.
- **Network Configuration**: Connected to a backend network with IP address 172.16.111.10.

## Event Tagger DYGI Service

- **Image**: ern_services_event_tagger_dygi:latest
- **Description**: Handles event tagging.
- **Resource Limits**: Constrained to 6 CPUs and 8GB of memory.
- **Dependencies**: Depends on RabbitMQ service.
- **Network Configuration**: Connected to the backend network with IP address 172.16.111.11.
- **Volumes**: Mounts directories for service files and cron jobs.
- **Environment Variables**: Loaded from `dygi_service.env`.

### AllenNLP Event Prediction Script

This script utilizes AllenNLP to perform event prediction on a set of documents.

### Overview

The script uses AllenNLP's command-line interface to run predictions using a pre-trained model on a specified input file containing documents in JSONL format. The predicted events are then written to an output file in JSONL format.

### Usage

To run the script, follow these steps:

1. Ensure you have AllenNLP installed. If not, you can install it via pip:

2. Navigate to the directory containing the script.

3. Update the `model`, `input`, and `output` variables in the script to point to your model file, input data file, and desired output file, respectively.

4. Run the script using Python:

### Command Assembly

The script assembles the command to be executed using AllenNLP's command-line interface. The command is constructed using the `sys.argv` list, with the following components:

- Command name (`"allennlp"`): Not used by AllenNLP's `main` function.
- Subcommand (`"predict"`): Indicates the task to be performed.
- Model file (`model`): Specifies the path to the pre-trained model file.
- Input file (`input`): Specifies the path to the input data file.
- Additional options:
- `"--predictor", "dygie"`: Specifies the predictor to be used (event predictor).
- `"--include-package", "dygie"`: Includes the package for the DyGIE model.
- `"--use-dataset-reader"`: Specifies to use the dataset reader.
- `"--output-file", output`: Specifies the path to the output file.
- `"--cuda-device", "-1"`: Specifies the CUDA device to use ("-1" indicates CPU).
- `"--silent"`: Suppresses AllenNLP's logging output.

### AllenNLP Command Execution

Finally, the script calls AllenNLP's `main` function, passing the assembled command as arguments. This executes the command, performing event prediction on the input data using the specified model and parameters.



## DYGI Handler Service

- **Image**: ern_services_dygi_handler:latest
- **Description**: Handles DYGI events.
- **Dependencies**: Depends on RabbitMQ service.
- **Network Configuration**: Connected to the backend network with IP address 172.16.111.12.
- **Volumes**: Mounts directories for service files.
- **Environment Variables**: Loaded from `dygi_handler.env`.

## API Gateway Service

- **Image**: ern_services_api_gateway:latest
- **Description**: Provides an API gateway for external access.
- **Dependencies**: Depends on RabbitMQ service.
- **Ports**: Exposes port 8002 for external access.
- **Network Configuration**: Connected to the backend network with IP address 172.16.111.13.
- **Volumes**: Mounts directories for service files.
- **Environment Variables**: Loaded from `api_gateway.env`.

## Network Configuration

All services are connected to a backend network with IP addresses assigned to facilitate internal communication.

## Usage

To deploy the microservices, execute the following command from the project root directory:


This will build and launch all microservices defined in the `docker-compose.yml` file. Ensure Docker and Docker Compose are installed on your system.

## Additional Components

- **dygi_service**: Contains the Event Tagger DYGI service.
- **dygi_handler_service**: Contains the DYGI Handler service.
- **api_gateway_service**: Contains the API Gateway service.


