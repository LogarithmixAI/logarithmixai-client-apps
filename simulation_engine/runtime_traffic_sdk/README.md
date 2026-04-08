# Runtime Traffic SDK

`runtime_traffic_sdk` is the runtime request-generation component inside the simulation engine area of this project. It is designed for internal development use and is responsible for sending realistic website traffic to client applications, monitoring responses, and generating high-volume runtime behavior that looks closer to real user activity.

## Purpose

- Generate runtime traffic against client websites and test targets
- Simulate realistic request flow with configurable load behavior
- Monitor request and response behavior during simulation
- Support internal development, telemetry generation, and observability validation

## What This Component Is

This is the runtime-facing traffic simulation SDK layer. It is the part of the simulation system that actively sends requests to target applications and behaves like a configurable client-side traffic engine.

It should be understood separately from the synthetic and chaos-oriented simulation work in:

- [synthetic_traffic_lab](/C:/Users/DeLL/Desktop/Ai-assistant-distributors/AI-Assisted-Distributed-Log-Monitoring-System/client_apps/simulation_engine/synthetic_traffic_lab)

## Current Package Identity

- Package name: `traffic_simulator`
- Version: `1.1.0`
- Main import:

```python
from traffic_simulator import TrafficSimulator
```

## Example Usage

```python
from traffic_simulator import TrafficSimulator

sim = TrafficSimulator(
    base_url="http://127.0.0.1:5000",
    users=5,
    duration=30,
    max_concurrency=4,
    debug=True,
    user_request_rate=5,
    load_profile=[
        (10, 2),
        (5, 9),
        (3, 15),
        (10, 3),
    ],
)

sim.start()
```

## Folder Structure

```text
runtime_traffic_sdk/
├── traffic_simulator/
├── examples/
├── pyproject.toml
└── README.md
```

## Main Areas

- `traffic_simulator/`
  core runtime package
- `examples/`
  usage examples for local development and validation
- `pyproject.toml`
  package metadata and dependency definition

## Development Positioning

This component is currently intended for internal development and data generation workflows. It is not being treated as a public package at this stage. The focus is:

- runtime realism
- configurable request behavior
- response monitoring
- development-time telemetry generation

## Notes

- This folder is the runtime-oriented traffic SDK side of the simulation engine.
- It should remain clean and reusable even if it stays inside the main project repo.
- If needed in the future, this component can be extracted into a separate repository with minimal restructuring.
