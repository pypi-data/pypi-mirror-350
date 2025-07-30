from typing import Optional, Dict, Any


class N8nClientError(Exception):
    """n8n 客戶端錯誤"""
    def __init__(
        self,
        message: str,
        details: Optional[Dict[str, Any]] = None
    ):
        self.details = details or {}
        super().__init__(message)


class N8nAPIError(N8nClientError):
    """n8n API 通信錯誤"""
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message, details)

class ToolExecutionError(N8nClientError):
    """MCP 工具執行錯誤"""
    def __init__(
        self,
        message: str,
        tool_name: Optional[str] = None,
        params: Optional[Dict[str, Any]] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        self.tool_name = tool_name
        self.params = params
        super().__init__(message, details)

class AuthenticationError(N8nClientError):
    """認證錯誤"""
    pass

class ConfigurationError(N8nClientError):
    """配置錯誤"""
    pass

class ResourceNotFoundError(N8nClientError):
    """資源未找到錯誤"""
    pass

class ValidationError(N8nClientError):
    """資料驗證錯誤"""
    pass 