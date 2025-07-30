"""
FlyWing API Client

This module provides a client for interacting with the FlyWing advertising system API.
"""

import json
import requests
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
import dataclasses
from dataclasses import is_dataclass

from .models import (
    ProxyInfo, ProxyConfig, Domain, Task, TaskCheckReq, TaskDetailCreateReq,
    TaskCreateReq, TaskReceiveListReq, TaskReceiveListResp, TaskReceiveReq,
    TaskReceiveResp, TaskUpdateWindowInfoReq, WorkingTime, ClientUser,
    UserRegisterReq, UserLoginResp, AutoTask, AutoTaskLog, AutoTaskUpdateResp
)


class EnhancedJSONEncoder(json.JSONEncoder):
    """Enhanced JSON encoder that handles dataclasses and datetime objects."""

    def default(self, obj):
        if is_dataclass(obj):
            return {k: v for k, v in dataclasses.asdict(obj).items() if v is not None}
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class FlyWingClient:
    """Client for interacting with the FlyWing advertising system API."""

    def __init__(self, base_url: str = "http://localhost:8080", token: Optional[str] = None):
        """Initialize the FlyWing API client.

        Args:
            base_url: The base URL of the FlyWing API.
            token: Optional authentication token.
        """
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()

    def _get_headers(self) -> Dict[str, str]:
        """Get the headers for API requests including authentication token if available."""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["token"] = self.token
        return headers

    def _request(self, method: str, path: str, data: Any = None, params: Dict[str, Any] = None) -> Any:
        """Send an HTTP request to the FlyWing API and return the response.

        Args:
            method: HTTP method (GET, POST, etc.).
            path: API endpoint path.
            data: Optional request data.
            params: Optional URL parameters.

        Returns:
            The parsed JSON response data.

        Raises:
            requests.HTTPError: If the request failed.
            ValueError: If the response does not contain a valid JSON structure.
        """
        url = f"{self.base_url}{path}"
        headers = self._get_headers()

        print(f'headers: {headers}')

        # Convert dataclass to dict for serialization
        if data and hasattr(data, 'to_dict'):
            data = data.to_dict()

        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            params=params
        )

        response.raise_for_status()

        if not response.content:
            return None

        result = response.json()

        # 验证响应格式是否符合预期
        if "code" not in result or "data" not in result:
            raise ValueError(f"Invalid API response format: {result}")

        # 检查响应状态码
        if result["code"] != 200:
            error_message = result.get("message", "Unknown error")
            raise ValueError(f"API error: {error_message} (Code: {result['code']})")

        # 返回实际的数据部分
        return result["data"]

    # User Management APIs
    def login(self, username: str, password: str) -> UserLoginResp:
        """User login with username and password.

        Args:
            username: The username of the user.
            password: The password of the user.

        Returns:
            UserLoginResp containing the user info and token.
        """
        params = {
            "username": username,
            "password": password
        }
        response = self._request("POST", "/api/user/login", params=params)

        # Update the client token for future requests
        if response and "token" in response:
            self.token = response["token"]

        # 使用from_dict方法创建实例
        return UserLoginResp.from_dict(response) if response else None

    def register(self, register_req: UserRegisterReq) -> UserLoginResp:
        """Register a new user.

        Args:
            register_req: User registration request with user details.

        Returns:
            UserLoginResp containing the user info and token if registration successful.
        """
        response = self._request("POST", "/api/user/register", data=register_req)

        # Update the client token for future requests
        if response and "token" in response:
            self.token = response["token"]

        # 使用from_dict方法创建实例
        return UserLoginResp.from_dict(response) if response else None

    def set_token(self, token: str) -> None:
        """Set the authentication token for the client.

        Args:
            token: The authentication token.
        """
        self.token = token
        self.session.headers.update({"token": token})

    def get_user_info(self) -> ClientUser:
        """Get the current authenticated user's information.

        Returns:
            ClientUser object containing user details.
        """
        response = self._request("GET", "/api/user/userinfo")
        return ClientUser.from_dict(response) if response else None

    # Proxy APIs
    def get_proxy_config_list(self) -> List[ProxyConfig]:
        """Get list of proxy configurations.

        Returns:
            List of ProxyConfig objects.
        """
        response = self._request("GET", "/api/proxy/list")
        return [ProxyConfig.from_dict(config) for config in response] if response else []

    def get_proxy_config_by_id(self, config_id: int) -> ProxyConfig:
        """Get proxy configuration by id.

        Args:
            config_id: The ID of the proxy configuration.

        Returns:
            ProxyConfig object for the specified ID.
        """
        response = self._request("GET", f"/api/proxy/{config_id}")
        return ProxyConfig.from_dict(response) if response else None

    def gen_proxy(self, config_id: int, count: int) -> List[ProxyInfo]:
        """Generate proxies from specified configuration.

        Args:
            config_id: The ID of the proxy configuration.
            count: Number of proxies to generate.

        Returns:
            List of ProxyInfo objects.
        """
        response = self._request("GET", f"/api/proxy/genProxy/{config_id}/{count}")
        return [ProxyInfo.from_dict(proxy) for proxy in response] if response else []

    # Task APIs
    def check_task(self, check_req: TaskCheckReq) -> Task:
        """Check a task by name and group ID.

        Args:
            check_req: Task check request with group ID and task name.

        Returns:
            Task object if found.
        """
        response = self._request("POST", "/api/task/check", data=check_req)
        return Task.from_dict(response) if response else None

    def create_task(self, create_req: TaskCreateReq) -> Task:
        """Create a new task.

        Args:
            create_req: Task creation request with task details.

        Returns:
            Created Task object.
        """
        response = self._request("POST", "/api/task/create", data=create_req)
        return Task.from_dict(response) if response else None

    def receive_task(self, receive_req: TaskReceiveReq) -> TaskReceiveResp:
        """Receive a task assignment.

        Args:
            receive_req: Task receive request with task criteria.

        Returns:
            TaskReceiveResp with assigned task details.
        """
        response = self._request("POST", "/api/task/receive", data=receive_req)
        return TaskReceiveResp.from_dict(response) if response else None

    def get_task_list(self, request_list: List[TaskReceiveListReq]) -> List[TaskReceiveListResp]:
        """Get list of tasks matching the criteria.

        Args:
            request_list: List of task receive list requests.

        Returns:
            List of TaskReceiveListResp objects.
        """
        response = self._request("POST", "/api/task/receive/list", data=request_list)
        return [TaskReceiveListResp.from_dict(task) for task in response] if response else []

    def update_complete_info(self, task_detail_id: int) -> None:
        """Update task completion information.

        Args:
            task_detail_id: ID of the task detail to mark as complete.
        """
        self._request("POST", f"/api/task/receive/update/complete/{task_detail_id}")

    def update_window_info(self, update_req: TaskUpdateWindowInfoReq) -> int:
        """Update task window information.

        Args:
            update_req: Task update window info request.

        Returns:
            Status code (typically 1 for success).
        """
        return self._request("POST", "/api/task/receive/update_window", data=update_req)

    # Working Time APIs
    def get_all_working_times(self) -> List[WorkingTime]:
        """Get list of all working time configurations.

        Returns:
            List of WorkingTime objects.
        """
        response = self._request("GET", "/api/working-time/all")
        return [WorkingTime.from_dict(time) for time in response] if response else []

    # Auto Task APIs
    def find_unfinished_auto_tasks(self) -> List[AutoTask]:
        """Get list of all unfinished automatic tasks.

        Returns:
            List of AutoTask objects representing unfinished tasks.
        """
        response = self._request("GET", "/api/autotask/findUnfinishedTasks")
        return [AutoTask.from_dict(task) for task in response] if response else []

    def upload_auto_task_log(self, task_log: AutoTaskLog) -> AutoTaskUpdateResp:
        """Upload a task log entry.

        Args:
            task_log: The AutoTaskLog object containing log details.

        Returns:
            AutoTaskUpdateResp object with operation status.
        """
        response = self._request("POST", "/api/autotask/uploadTaskLog", data=task_log)
        return AutoTaskUpdateResp.from_dict(response) if response else None

    def get_auto_task_log_by_id(self, task_id: int) -> AutoTaskUpdateResp:
        """Get task log by task ID.

        Args:
            task_id: ID of the task to retrieve log for.

        Returns:
            AutoTaskUpdateResp object containing task log information.
        """
        response = self._request("GET", f"/api/autotask/{task_id}")
        return AutoTaskUpdateResp.from_dict(response) if response else None
