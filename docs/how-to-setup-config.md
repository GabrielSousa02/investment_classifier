# Config file setup

## What is this file for

This file will set **most** of the important parameters in the application.

> This repo comes with a pre-built `config.yaml`,
> you can find it [here](../config.yaml).

> [!IMPORTANT]
> Don't forget to add your input/output directory, and to add your dataset!

## Parameters' definition

Here's a breakdown of the parameters:

### Application level

| Parameter                | Default | Description                                                                                                   |
|--------------------------|---------|---------------------------------------------------------------------------------------------------------------|
| name                     | None    | This is the application/project name.                                                                         |
| version                  | None    | This is a simple version tag for the system in general.                                                       |
| description              | None    | This is a brief description of the project's purpose.                                                         |
| classification_engine    | static  | This field can be "static" or "dynamic", it determines which set of rules it will use to classify the dataset |
| data_sanitizing_strategy | 1       | 0 to remove rows that are data inconsistent, 1 to use empty value of column type                              |

### Data Source Configuration

| Parameter        | Default        | Description                                        |
|------------------|----------------|----------------------------------------------------|
| input_base_path  | "data/input/"  | From project directory, but can be set to any dir. |
| output_base_path | "data/output/" | From project directory, but can be set to any dir. |
| input_filename   | None           | Specify your file name                             |

### Logging Configuration

| Parameter | Default        | Description                                        |
|-----------|----------------|----------------------------------------------------|
| level     | "INFO"         | Standard log level of the project                  |
| file_path | "logs/app.log" | From project directory, but can be set to any dir. |

