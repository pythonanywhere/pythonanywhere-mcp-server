import pytest

@pytest.fixture
def mcp():
    class MockMCP:
        def __init__(self):
            self._tools = {}
        def tool(self, name=None, **kwargs):
            def decorator(fn):
                tool_name = name or fn.__name__
                self._tools[tool_name] = fn
                return fn
            return decorator
        def call_tool(self, name, arguments):
            fn = self._tools[name]
            return fn(**arguments)
    return MockMCP()

