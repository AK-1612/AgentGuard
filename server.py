from fastapi import FastAPI, HTTPException
from schemas import ToolExecutionRequest
from middleware import AgentGuardMiddleware

app = FastAPI(title="AgentGuard Security Proxy", version="1.0.0")
guard = AgentGuardMiddleware()

@app.post("/api/v1/execute-tool")
async def execute_tool(request: ToolExecutionRequest):
    evaluation = guard.intercept(request)
    
    if evaluation.status == "BLOCK":
        # Return HTTP 403 Forbidden with strict schema
        raise HTTPException(
            status_code=403, 
            detail={"error_code": evaluation.error_code, "reason": evaluation.reason}
        )
        
    # In a real app, route to the actual tool execution here
    return {
        "status": "success",
        "executed_tool": request.tool_name,
        "message": "Security checks passed. Tool executed successfully."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)