# IPC Snippets with SimPy

Snippets of Inter-process Communication (IPC) with [SimPy](https://simpy.readthedocs.io/en/latest/) simulation environments.

## Folder structure

- _request-response-comm_ contains an example of _Request-response_ communication with reply, built with [ZeroMQ](https://zeromq.org/) messaging library, between a server running a **real-time** SimPy simulation environment and a client interrogating the server to affect the on-going simulation. Such a solution allows the creation of public APIs able to interrogate a running SimPy simulation, mimicking the interaction with a remote digital twin.

- _sync-sim-branches_
