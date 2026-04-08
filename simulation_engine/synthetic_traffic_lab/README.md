# Synthetic Traffic Lab

`synthetic_traffic_lab` is the synthetic and chaos-oriented simulation component inside the simulation engine area of this project. It is intended for internal development, anomaly experiments, session modeling, traffic spikes, and behavior generation that supports log creation, pattern testing, and failure-oriented observability validation.

## Purpose

- Generate synthetic traffic behavior for development and testing
- Simulate session-based activity patterns
- Create spike and burst scenarios
- Support chaos-style simulation and anomaly-oriented experiments
- Produce structured synthetic behavior for internal data and log generation

## What This Component Is

This is the experiment-oriented and scenario-oriented side of the traffic simulation system. It is different from the runtime request SDK because its focus is synthetic modeling and chaos behavior rather than direct runtime client request execution.

It should be understood separately from:

- [runtime_traffic_sdk](/C:/Users/DeLL/Desktop/Ai-assistant-distributors/AI-Assisted-Distributed-Log-Monitoring-System/client_apps/simulation_engine/runtime_traffic_sdk)

## Current Package Identity

- Package name: `simulator_sdk`
- Version: `0.1.0`
- Main exports:

```python
from simulator_sdk import SessionSimulator, TrafficSpike, ChaosEngine
```

## Main Exposed Components

- `SessionSimulator`
  session-style synthetic behavior generation
- `TrafficSpike`
  spike and burst traffic simulation
- `ChaosEngine`
  controlled anomaly and chaos behavior generation

## Folder Structure

```text
synthetic_traffic_lab/
├── simulator_sdk/
├── pyproject.toml
└── README.md
```

## Internal Areas

- `simulator_sdk/simulation/`
  simulation logic for sessions, spikes, and chaos
- `simulator_sdk/traffic/`
  traffic behavior generation helpers
- `simulator_sdk/error_patterns/`
  synthetic error and anomaly pattern definitions

## Development Positioning

This component is currently intended for internal use. It works as a synthetic behavior lab for generating test scenarios and supporting anomaly-related development workflows.

Primary focus areas:

- scenario generation
- anomaly experiments
- session behavior modeling
- traffic spike simulation
- internal development-time log generation

## Notes

- This folder is the synthetic and chaos-oriented side of the simulation engine.
- It complements the runtime request-focused SDK rather than replacing it.
- If the project matures further, this component can later be expanded into a more formal internal simulation toolkit.
