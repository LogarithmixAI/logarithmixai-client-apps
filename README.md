# LogarithmixAI Client Apps

`client_apps` is the application-side workspace used to generate telemetry, traffic, runtime behavior, and testing data for the broader LogarithmixAI monitoring platform.

This repository area is not the backend system itself. It is the source side of the ecosystem where websites, demo clients, and traffic simulation components generate realistic application activity for SDK validation, telemetry collection, anomaly testing, and observability development.

## What This Repository Contains

- Flask-based demo and client applications
- Client-side telemetry generation targets
- Runtime traffic generation utilities
- Synthetic and chaos-oriented traffic simulation components
- Templates and examples used to exercise the monitoring pipeline

## Main Areas

```text
client_apps/
├── app.py
├── client_app.py
├── client_app1.py
├── client_app2.py
├── client_test.py
├── templates/
├── simulation_engine/
│   ├── runtime_traffic_sdk/
│   └── synthetic_traffic_lab/
└── simulation_notebook.ipynb
```

## Role In The Platform

This repository supports the platform by acting as the telemetry source layer.

- Client apps generate real request and response activity
- SDK-integrated applications emit monitoring events
- Simulation components create runtime, synthetic, and chaos traffic
- These sources help validate the SDK, backend telemetry pipeline, and anomaly workflows

## Simulation Engine

The simulation area contains two distinct internal components:

- `runtime_traffic_sdk`
  runtime request generation for realistic application traffic
- `synthetic_traffic_lab`
  synthetic behavior, session modeling, spike generation, and chaos-style simulation

## Intended Use

This repository is primarily for internal development and integration workflows.

- generate telemetry from realistic app usage
- simulate different request and error conditions
- validate monitoring behavior
- produce development-time data for observability analysis

## Ownership

- Organization: [LogarithmixAI](https://github.com/LogarithmixAI)
- Public author identity: `ShubhamCoder-In`

## Notes

- This repository can later be split further if client applications and simulation tooling need independent release cycles.
- For now, keeping them together is useful because both sides contribute to the same telemetry-generation workflow.
