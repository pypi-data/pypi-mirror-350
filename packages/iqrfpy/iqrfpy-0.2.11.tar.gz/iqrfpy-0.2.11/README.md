## What is iqrfpy?

iqrfpy is a library that provides a python API for interacting with the IQRF network
utilizing the [DPA framework](https://doc.iqrf.org/DpaTechGuide/) (DPA) or IQRF Gateway Daemon (Daemon) [JSON API](https://docs.iqrf.org/iqrf-gateway/user/daemon/api). Communication between a python runtime and the IQRF network is facilitated by transports.

For communication with Daemon, only the MQTT transport is implemented at this time.
However, this library provides an abstract transport class, allowing for custom communication implementations.

The library provides classes for serialization of requests and deserialization of responses to message class objects.

## Quick start

Before installing the library, it is recommended to first create a virtual environment.
Virtual environments help isolate python installations as well as pip packages independent of the operating system.

A virtual environment can be created and launched using the following commands:

```bash
python3 -m venv <dir>
source <dir>/bin/activate
```

iqrfpy can be installed using the pip utility:

```bash
python3 -m pip install -U iqrfpy
```

### Serialize requests to DPA:
```python
from iqrfpy.peripherals.coordinator.requests.addr_info import AddrInfoRequest

req = AddrInfoRequest()
req_packet = req.to_dpa()
print(req_packet)
```

### Serialize requests to JSON:
```python
from iqrfpy.peripherals.coordinator.requests.addr_info import AddrInfoRequest

req = AddrInfoRequest()
json_req = req.to_json()
print(json_req)
```

### Parse DPA responses:
```python
from iqrfpy.peripherals.coordinator.responses import AddrInfoResponse
from iqrfpy.response_factory import ResponseFactory

def handle_addr_info_response(response: AddrInfoResponse) -> None:
    print(f'peripheral: {response.pnum}')
    print(f'peripheral command: {response.pcmd}')
    status = response.rcode
    if status == 0:
        print(f'Addr info response dev_nr: {response.dev_nr}')
        print(f'Addr info response did: {response.did}')


dpa_rsp_packet = b'\x00\x00\x00\x80\x00\x00\x00\x40\x0a\x2a'
dpa_rsp = ResponseFactory.get_response_from_dpa(dpa=dpa_rsp_packet)
handle_addr_info_response(response=dpa_rsp)
```

### Parse JSON responses:
```python
from iqrfpy.peripherals.coordinator.responses import AddrInfoResponse
from iqrfpy.response_factory import ResponseFactory

def handle_addr_info_response(response: AddrInfoResponse) -> None:
    print(f'peripheral: {response.pnum}')
    print(f'peripheral command: {response.pcmd}')
    status = response.rcode
    if status == 0:
        print(f'Addr info response dev_nr: {response.dev_nr}')
        print(f'Addr info response did: {response.did}')


daemon_rsp_json = {
    "mType": "iqrfEmbedCoordinator_AddrInfo",
    "data": {
        "msgId": "testEmbedCoordinator",
        "rsp": {
            "nAdr": 0,
            "hwpId": 0,
            "rCode": 0,
            "dpaVal": 64,
            "result": {
                "devNr": 0,
                "did": 42
            }
        },
        "insId": "iqrfgd2-1",
        "status": 0
    }
}
json_rsp = ResponseFactory.get_response_from_json(json=daemon_rsp_json)
handle_addr_info_response(response=json_rsp)
```

## Documentation

For more information, check out our [API reference](https://apidocs.iqrf.org/iqrfpy/latest/iqrfpy.html).
