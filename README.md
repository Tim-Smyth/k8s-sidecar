# What?

This is a docker container intended to run inside a kubernetes cluster to collect config maps with a specified label and store the included files in an local folder. The main target is to be run as a sidecar container to supply an application with information from the cluster.

# Why?

Currently (April 2018) there is no simple way to hand files in configmaps to a service and keep them updated during runtime.

# How?

Run the container created by this repo together you application in an single pod with a shared volume. Specify which label should be monitored and where the files should be stored.

# Features

- Extract files from config maps
- Filter based on label
- Update/Delete on change of configmap

# Usage

## Configuration Environment Variables

- `LABEL` 
  - description: Label that should be used for filtering
  - required: true
  - type: string

- `FOLDER`
  - description: Folder where the files should be placed
  - required: true
  - type: string