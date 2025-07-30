# Apex Nova Python Stubs

This repository contains Python stubs generated from gRPC protobuf definitions for Apex Nova services.

## Overview

The stubs are generated using `protoc` and the `grpc_tools` package, which provides the necessary tools to compile `.proto` files into Python code. These stubs include both the protocol buffer message classes and the gRPC service classes.

## Directory Structure

The directory structure of this repository is as follows:

```
python-stub/
├── build.gradle.kts
├── README.md
├── src/
│   ├── apexnova/
│   │   ├── __init__.py
│   ├── ...
```

## Usage

To use the stubs in your Python project, you can install them from PyPI using the following command:

```
pip install apexnova-stubs
```
