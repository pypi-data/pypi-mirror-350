# FCT-Kiwi

A command-line tool for Balena device configuration management, allowing you to easily change, clone, purge, retrieve, and manage variables across devices and fleets.

## Table of Contents

- [FCT-Kiwi](#fct-kiwi)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Authentication](#authentication)
    - [Environment variables](#environment-variables)
  - [Commands](#commands)
    - [Usage in other scripts](#usage-in-other-scripts)
    - [Change](#change)
    - [Clone](#clone)
    - [Purge](#purge)
    - [Get](#get)
    - [Delete](#delete)
    - [Move](#move)
    - [Schedule](#schedule)
      - [Schedule change](#schedule-change)
      - [Schedule update](#schedule-update)
    - [Initialize](#initialize)
    - [Rename](#rename)
  - [File Format](#file-format)
    - [Changing variables](#changing-variables)
    - [Scheduling](#scheduling)
      - [Variable changes](#variable-changes)
      - [Pin devices to release](#pin-devices-to-release)
    - [Tags by version](#tags-by-version)
  - [Error Handling](#error-handling)
  - [Dependencies](#dependencies)
  - [Author](#author)

## Installation

```bash
pip install fct-kiwi
```

## Authentication

To use this tool, you need to set up some environment variables if you haven't already, please refer to the [Environment variables](#environment-variables) section to set all the variables that don't have a default, this can be done in your terminal as environment variables, for example:

`export BALENA_API_KEY="your_api_key_here"`

Or an environment variables file to handle all at once can be defined as shown in the next section.

### Environment variables

By default this is the order in which variables are read:

1. `.env` file
2. default
3. os.environ

Other variables might be needed for certain commands and are set by default, but can be overridden if necessary.

1. Create a `.env` file in the same directory as the script or set the path into your environment as `export FCT_ENV_PATH="/path/to/my/.env"`
2. Add your Balena API key: `BALENA_API_KEY=your_api_key_here`
3. Add other variables in new lines, this is a list of all variables used:

| Variable                        | Description                    | Default                                    |
| ----------------------          | ----------------------------   | ------------------------------------------ |
|`BALENA_API_KEY`                 | Balena API key                 |                                            |
|`PROJECT_ID`                     | GCP Project                    |                                            |
|`SPREADSHEET_NAME`               | Google Sheets file for logging | SD Logs                                    |
|`LOCATION_ID`                    | GCP Queue location             |                                            |
|`QUEUE_ID`                       | GCP Queue identifier           |                                            |
|`AUTHOR`                         | Google Sheets author signature | default                                    |
|`ORGANIZATION_HANDLE`            | Balena Organization Handle     |                                            |
|`GOOGLE_APPLICATION_CREDENTIALS` | GCP Service account file       | serviceAccountKey.json                     |
|`TAGS_BY_VERSION_FILE`           | Tags by version file location  | tags_by_version.json                       |

## Commands

### Usage in other scripts

To use this packages functionality in other scripts simply import the functions you need from the following list.

```python
from fleet_control import clone, change, etc...
```

Otherwise you can use all commands from your terminal.

### Change

Change or create specified variable(s) to target device(s).

```bash
# Basic usage
fct change 'VAR_NAME=0=*' 4X002 4X003

# Change multiple variables
fct change 'VAR_NAME=0=* ANOTHER_VAR=value=service_name' 4X002 4X003

# Target a fleet
fct change 'VAR_NAME=0=*' FLEET_NAME

# Use a file containing variables
fct change --file variables.txt '' 4X002 4X003
```

### Clone

Clone configuration from a source device or fleet to target device(s).

```bash
# Clone from one device to others
fct clone 4X001 4X002 4X003

# Clone from a fleet to a device
fct clone FLEET_NAME 4X002

# Clone from a fleet to another fleet
fct clone FLEET_NAME ANOTHER_FLEET_NAME

# Clone with exclusions
fct clone --exclude "VAR1 VAR2" 4X001 4X002 4X003
```

### Purge

Purge all custom variables in target device(s).

```bash
# Purge all custom variables from devices
fct purge 4X001 4X002 4X003

# Purge with exclusions
fct purge --exclude "VAR1 VAR2" 4X001 4X002 4X003
```

### Get

Fetch variable value(s) for a device.

```bash
# Get a specific variable
fct get 4X001 VAR_NAME

# Get all custom variables
fct get 4X001 --custom

# Get all variables (device + fleet)
fct get 4X001 --all-vars

# Save variables to a file
fct get 4X001 --output result.json
```

### Delete

Delete the overwritten value for specified variable(s) on the target device(s).

```bash
# Delete a variable
fct delete 'VAR_NAME=0=*' 4X002 4X003

# Delete multiple variables
fct delete 'VAR1=value=service VAR2=value=*' 4X002 4X003

# Delete variables from a file
fct delete --file variables.txt '' 4X002 4X003
```

### Move

Move target(s) from its current fleet to a specified fleet.

```bash
# Move devices to a new fleet
fct move FLEET_NAME 4X001 4X002 4X003

# Move keeping custom device variables
fct move --keep-vars FLEET_NAME 4X001 4X002 4X003

# Move keeping custom device and service variables
fct move --keep-service-vars FLEET_NAME 4X001 4X002 4X003

# Move with cloning (keep custom and previous fleet variables)
fct move --clone FLEET_NAME 4X001 4X002 4X003

# Move and pin to specific release
fct move --semver "1.3.11+rev87" FLEET_NAME 4X001 4X002 4X003
```

### Schedule

Schedule functions to run at a specific time. Service account file path required for creating the task. Set with the `GOOGLE_APPLICATION_CREDENTIALS` variable set in the `.env` file or in your environment.

#### Schedule change

Change or create specified variable(s) to target device(s).

```bash
# Schedule a change for tomorrow at 3 AM (default)
fct schedule change 'VAR_NAME=0=main' 4X001 4X002

# Schedule with a specific date and time
fct schedule change --date '2025-02-25 12:06:00' 'VAR_NAME=0=main' 4X001 4X002

# Schedule with a file containing variables
fct schedule change --date '2025-02-25 12:06:00' --file vars.json 

# Schedule with different timezone
fct schedule change --tz 'America/New_York' 'VAR_NAME=0=main' 4X001 4X002
```

#### Schedule update

Pins the specified devices to the selected release in that fleet.

```bash
# Schedule a pin to release for tomorrow at 3 AM (default)
fct schedule update FLEET_NAME 1.3.19+rev43 4X001 4X002

# Direct input with date and timezone
fct schedule update --date '2025-04-01T15:30:00Z' --tz 'Europe/London' FLEET_NAME 1.3.19+rev43 4X001 

# Use a JSON file for targets and release info
fct schedule update --date '2025-02-25 12:06:00' --file file.json 
```

### Initialize

Initialize a target device with previous device tags, remove old device, delete default config variables, and move to specified fleet.

```bash
# Initialize a device and move it to a fleet
fct initialize FLEET_NAME 4X001
```

### Rename

Rename a target device with new ID. Optional new tags for corresponding version read from configuration file. Configuration file path set with the `TAGS_BY_VERSION_FILE` variable set in the `.env` file or in your environment.

```bash
# Rename a device
fct rename 4A001 4B222

# Rename a device and specify new version
fct rename --version "4.3F" 4A001 4B222
```

## File Format

### Changing variables

When using the `--file` option, the file should contain JSON formatted variables:

```json
{
  "env_vars": {
      "VAR1_NAME": "VAR1_VALUE",
      "VAR2_NAME": 2
  },
  "service_vars": {
      "main": {
        "SERVICE_VAR1_NAME": "SERVICE_VAR1_VALUE",
        "SERVICE_VAR2_NAME": "SERVICE_VAR2_VALUE"
      }
  }
}
```

### Scheduling

#### Variable changes

```json
{
  "targets": [
    "TARGET1_NAME",
    "TARGET2_NAME"
  ],
  "variables": {
    "env_vars": {
        "VAR1_NAME": "VAR1_VALUE",
        "VAR2_NAME": 2
    },
    "service_vars": {
        "main": {
          "SERVICE_VAR1_NAME": "SERVICE_VAR1_VALUE",
          "SERVICE_VAR2_NAME": "SERVICE_VAR2_VALUE"
        }
    }
  }
}
```

#### Pin devices to release

```json
{
    "targets": [
        "TARGET1_NAME",
        "TARGET2_NAME"
    ],
    "fleet": "FLEET_NAME",
    "release": "RELEASE_SEMVER"
}
```

### Tags by version

```json
{
    "4.3B":{
        "Tag1": "value1",
        "Tag2": "value2",
    }
}
```

## Error Handling

The tool will return appropriate error messages if:

- The Balena API key is not set
- No variables are provided when required
- Target devices or fleets cannot be found
- API requests fail

## Dependencies

- balena-sdk
- click
- python-dotenv

## Author

Juan Pablo Castillo - <juan.castillo@kiwibot.com>
