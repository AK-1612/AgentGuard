import logging
from schemas import ToolExecutionRequest, SecurityEvaluation
from scanner import SecurityScanner

logger = logging.getLogger("AgentGuard")
logger.setLevel(logging.INFO)

class AgentGuardMiddleware:
    def __init__(self, enable_semantics: bool = True):
        self.scanner = SecurityScanner(use_semantics=enable_semantics)

    def intercept(self, request: ToolExecutionRequest) -> SecurityEvaluation:
        logger.info(f"Scanning tool execution: {request.tool_name}")

        if request.raw_prompt:
            is_safe, err_code, reason = self.scanner.scan_prompt(request.raw_prompt)
            if not is_safe:
                logger.warning(f"BLOCKED: {err_code} - {reason}")
                return SecurityEvaluation(status="BLOCK", error_code=err_code, reason=reason)

        is_safe, err_code, reason = self.scanner.scan_arguments(request.tool_name, request.arguments)
        if not is_safe:
            logger.warning(f"BLOCKED: {err_code} - {reason}")
            return SecurityEvaluation(status="BLOCK", error_code=err_code, reason=reason)

        return SecurityEvaluation(status="ALLOW")