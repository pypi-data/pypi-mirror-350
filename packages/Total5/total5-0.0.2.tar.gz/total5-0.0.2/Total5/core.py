import socket
import struct
import sys
import json
import inspect
from collections import defaultdict

def recv_exact(conn, size):
	buf = b''
	while len(buf) < size:
		chunk = conn.recv(size - len(buf))
		if chunk:
			buf += chunk
	return buf

class TotalCore:

	def __init__(self):
		self.handlers = defaultdict(list)
		self.client = None

	def on(self, name):
		def decorator(fn):
			self.handlers[name].append(fn)
			return fn
		return decorator

	def emit(self, name, *args):
		handlers = self.handlers.get(name, [])
		if not handlers:
			return
		for fn in handlers:
			sig = inspect.signature(fn)
			count = len(sig.parameters)
			fn(*args[:count])

	def send(self, data):

		if not self.client:
			self.emit("error", "Not connecterd")

		if isinstance(data, dict) or isinstance(data, list):
			payload = json.dumps(data).encode()
		elif isinstance(data, str):
			payload = data.encode()
		elif isinstance(data, (bytes, bytearray)):
			payload = data
		else:
			self.emit("error", "Unsupported payload type")
			return

		length = len(payload)
		header = struct.pack('>I', length)

		self.client.sendall(header + payload)
		return

	def listen(self, type = "json", path = None):

		if not path:
			if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
				path = sys.argv[1]

		if path is None:
			self.emit("error", "Socket is not specified")
			return

		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(path)

		while True:
			with self.client:
				try:
					self.emit("open")
					while True:
						# 4 bytes size + other message data
						header = recv_exact(self.client, 4)
						length = struct.unpack('>I', header)[0]
						data = recv_exact(self.client, length)

						if type == "json":
							try:
								parsed = json.loads(data.decode())
								self.emit("data", parsed)
							except Exception:
								self.emit("error", "JSON parser error")
						elif type == "text":
							self.emit("data", data.decode())
						else:
							self.emit("data", data)

				except ConnectionError:
					self.emit("error", "Connection error")
		return

singleton = TotalCore()
