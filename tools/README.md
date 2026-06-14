# Defensive Helper Tools

`tools/js/` contains dependency-free pure functions for static analysis. They
do not read files, inspect the process environment, create subprocesses, or make
network requests.

The helpers model:

- npm lifecycle script extraction;
- import graph traversal;
- loopback-only beacon serialization;
- network error classification;
- safe staged-response descriptions.

