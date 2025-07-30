# Total.js integration

The Total.js Python library provides a predefined integration between the Total.js framework (Pypelines) and Python scripts.

- [Website](https://totaljs.com)

```python
import Total5
import sys

@Total5.on('data')
def data(payload, uid):
	# @payload {JSON|String|Buffer} payload
	# @uid {Number} message identifier (optional)
	print("--->", payload, uid)

@Total5.on('open')
def open():
	# Total.js is connected

@Total5.on('close')
def close():
	# Total.js is disconnected

# Total5.send(payload, [uid]);
# @payload {JSON|String|Buffer} payload
# @uid {Number} message identifier (optional)
# IMPORTANT: This method must be performed while Total.js is connected.
Total5.send({ "name": "Hello world!"})

# Total.listen(type, socket_path)
# @type {json|text|buffer}
# @socket_path {String} path to the socket (optional)
Total5.listen("json", "/tmp/total.sock")
```

__Python on MacOS__:

```shell
python3 -m venv .venv
source .venv/bin/activate
```
