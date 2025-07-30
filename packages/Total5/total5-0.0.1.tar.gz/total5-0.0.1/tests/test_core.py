import Total5

def test_emit_event():

	result = []

	@Total5.on('data')
	def handler(data):
		result.append(data)

	Total5.emit('data', {'x': 123 })
	assert result == [{'x': 123}]
