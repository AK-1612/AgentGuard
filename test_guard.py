import pytest
from schemas import ToolExecutionRequest
from middleware import AgentGuardMiddleware

# Disable semantics for fast unit testing, test regex logic
@pytest.fixture
def guard():
    return AgentGuardMiddleware(enable_semantics=False)

def test_safe_execution(guard):
    req = ToolExecutionRequest(
        tool_name="execute_bash",
        arguments={"command": "ls -la"},
        raw_prompt="List files in this directory."
    )
    res = guard.intercept(req)
    assert res.status == "ALLOW"

def test_dangerous_command_blocked(guard):
    req = ToolExecutionRequest(
        tool_name="execute_bash",
        arguments={"command": "rm -rf /"},
        raw_prompt="Delete everything."
    )
    res = guard.intercept(req)
    assert res.status == "BLOCK"
    assert res.error_code == "ERR_UNAUTHORIZED_COMMAND"