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
		if not chunk:
			raise ConnectionError("[Total.js] Connection error")
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

	def send(self, data, uid: int = 0):

		if not self.client:
			raise ConnectionError("[Total.js] Not connected")

		if isinstance(data, dict) or isinstance(data, list):
			payload = json.dumps(data).encode()
		elif isinstance(data, str):
			payload = data.encode()
		elif isinstance(data, (bytes, bytearray)):
			payload = data
		else:
			raise TypeError(f"[Total.js] Unsupported payload type: {type(data)}")

		length = len(payload)
		header = struct.pack('>II', length, uid)

		self.client.sendall(header + payload)
		return

	def listen(self, type = "json", path = None):

		if not path:
			if len(sys.argv) > 1 and len(sys.argv[1]) > 0:
				path = sys.argv[1]

		if path is None:
			print("[Total.js] Socket is not specified")
			return

		self.client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
		self.client.connect(path)

		while True:
			with self.client:
				try:
					self.emit("open")
					while True:
						# 4 bytes size, 4 bytes UID, other message data
						header = recv_exact(self.client, 8)
						length, uid = struct.unpack('>II', header)
						data = recv_exact(self.client, length)

						if type == "json":
							try:
								parsed = json.loads(data.decode())
								self.emit("data", parsed, uid)
							except Exception as e:
								print("[Total.js] JSON parser error:", e)
						elif type == "text":
							self.emit("data", data.decode(), uid)
						else:
							self.emit("data", data, uid)


				except ConnectionError:
					print("[Total.js] Connection error")

		return

singleton = TotalCore()
