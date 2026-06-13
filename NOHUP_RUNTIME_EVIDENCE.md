# Reconstructed `nohup.out` Runtime Evidence

This file reconstructs the runtime evidence observed from the detached `node server` process during the live MetaPlay incident.

This is **not** the original preserved `nohup.out` file. It is a reconstructed excerpt based on the observed error, the known `socket/index.js` execution path, and the captured second-stage payload behavior.

## Reconstructed Error Excerpt

During the live run, the detached process produced runtime evidence consistent with the downloaded stage-two payload attempting to contact the direct-IP C2 endpoint and failing due to network unreachability.

The observed error was equivalent to:

```text
TypeError: fetch failed
    at node:internal/deps/undici/undici:<line>:<column>
    at process.processTicksAndRejections (node:internal/process/task_queues:<line>:<column>)
    at async send request (eval at <anonymous> (/home/arx/src/MetaPlay/socket/index.js:75:24), <anonymous>:3:3261) {
  [cause]: Error: connect ENETUNREACH 136.243.22.62:1224
      at TCPConnectWrap.afterConnect [as oncomplete] (node:net:<line>:<column>) {
    errno: -101,
    code: 'ENETUNREACH',
    syscall: 'connect',
    address: '136.243.22.62',
    port: 1224
  }
}
```

## Structured Interpretation

```json
{
  "runtime_error": "TypeError: fetch failed",
  "execution_context": {
    "source": "downloaded stage-two JavaScript",
    "executor": "new Function(\"require\", response.data)",
    "originating_file": "/home/arx/src/MetaPlay/socket/index.js",
    "originating_location": "socket/index.js:75:24",
    "evaluated_location": "<anonymous>:3:3261"
  },
  "network_error": {
    "code": "ENETUNREACH",
    "syscall": "connect",
    "address": "136.243.22.62",
    "port": 1224
  },
  "assessment": "The malicious loader reached the downloaded stage-two execution path. The direct-IP C2 connection attempt failed during the observed run."
}
```

## Inferred C2 Endpoint

Based on the captured stage-two script, the failed request was attempting to reach:

```text
http://136.243.22.62:1224/api/checkStatus
```

## Logical Beacon Fields

The request was constructed as a query-string beacon rather than a JSON POST body. Its logical payload was equivalent to:

```json
{
  "sysInfo": {
    "hostname": "<victim-hostname>",
    "type": "<os-type>",
    "release": "<os-release>",
    "platform": "<os-platform>",
    "mac": "<first-non-internal-ipv4-mac-address>"
  },
  "processInfo": {
    "...": "copy of process.env"
  },
  "tid": "<stage-two-token>",
  "sysId": "<stage-two-system-id>"
}
```

## Evidentiary Meaning

This error is important because it shows the live root `npm i` did more than trigger a local script. The execution chain advanced through the Vercel loader into the fetched stage-two payload.

However, the `ENETUNREACH` error strongly indicates that the observed direct-IP C2 request to `136.243.22.62:1224` did not complete.

The key evidence-bearing line is:

```text
at async send request (eval at <anonymous> (/home/arx/src/MetaPlay/socket/index.js:75:24), <anonymous>:3:3261)
```

That ties the runtime error back to downloaded code executed through `new Function` inside `socket/index.js`.
