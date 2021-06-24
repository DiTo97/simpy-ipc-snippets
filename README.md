# IPC Snippets with SimPy

Snippets of Inter-process Communication (IPC) with [SimPy](https://simpy.readthedocs.io/en/latest/) simulation environments.

## Folder structure

- _request-response-comm_, contains an example of _Request-response_ communication with reply, built with the messaging library [ZeroMQ](https://zeromq.org/), between a server running a **real-time** SimPy simulation environment and a client interrogating the server to affect the on-going simulation. Such a solution allows the creation of public APIs able to interrogate a running SimPy simulation, mimicking the interaction with a remote digital twin.

- _sync-sim-branches_, contains an example of synchronization between simultaneous instances of the same running SimPy environment: a process running a SimPy simulation is forked into a child process having a hold of the current state of the simulation. The child process runs its own version of the simulation without affecting the one hanging in the parent process and returns its final state to the latter. Such a solution allows the combination of a SimPy simulation with an online RL agent whose reward function does not depend on the instant consequences of its actions, but rather on the long-term effects its decisions have on the environment after Delta(t).
