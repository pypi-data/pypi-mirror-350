# NUA SDK

## Overview

The NUA SDK provides shared components and utilities for NUA security agents. This package serves as a foundation for building and extending NUA's security automation capabilities.

## Installation
You can install the NUA SDK by running:
```sh
pip install nua-sdk
```
## .env for authentication agent.
You must have this value in your .env to make sure the authentication agent will work properly
```sh
AUTH_AGENT_URL=auth agent deployment URL
```

## Use authentication agent
```sh
from nua_sdk import AuthenticationAgent
results = AuthenticationAgent(message=message).authenticate()
```
