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

        # 返回数据部分
        if result["code"] != 0:
            raise ValueError(f"API error: {result.get('msg', 'Unknown error')}")

        return result["data"]

    # User Management APIs
    def register(self, user_reg_req: UserRegisterReq) -> bool:
        """Register a new user.

        Args:
            user_reg_req: User registration request data.

        Returns:
            True if registration was successful, False otherwise.
        """
        response = self._request("POST", "/api/user/register", data=user_reg_req)
        return response is not None

    def login(self, username: str, password: str) -> UserLoginResp:
        """Login with username and password.

        Args:
            username: The username.
            password: The password.

        Returns:
            UserLoginResp object containing token and user info.
        """
        data = {"userName": username, "password": password}
        response = self._request("POST", "/api/user/login", data=data)
        if response:
            login_resp = UserLoginResp.from_dict(response)
            self.token = login_resp.token
            return login_resp
        return None

    # Proxy Management APIs
    def get_proxy_config_list(self) -> List[ProxyConfig]:
        """Get list of available proxy configurations.

        Returns:
            List of ProxyConfig objects.
        """
        response = self._request("GET", "/api/proxy/list")
        return [ProxyConfig.from_dict(config) for config in response] if response else []

    def get_proxy_config_by_id(self, config_id: int) -> ProxyConfig:
        """Get proxy configuration by ID.

        Args:
            config_id: ID of the proxy configuration.

        Returns:
            ProxyConfig object.
        """
        response = self._request("GET", f"/api/proxy/{config_id}")
        return ProxyConfig.from_dict(response) if response else None

    def generate_proxies(self, config_id: int, count: int) -> List[ProxyInfo]:
        """Generate proxies from a specific provider.

        Args:
            config_id: ID of the proxy configuration.
            count: Number of proxies to generate.

        Returns:
            List of ProxyInfo objects.
        """
        response = self._request("GET", f"/api/proxy/genProxy/{config_id}/{count}")
        return [ProxyInfo.from_dict(proxy) for proxy in response] if response else []

    # Task Management APIs
    def check_task_exists(self, task_check: TaskCheckReq) -> bool:
        """Check if a task with given group ID and name exists.

        Args:
            task_check: Request with group ID and task name.

        Returns:
            True if the task exists, False otherwise.
        """
        response = self._request("POST", "/api/task/check", data=task_check)
        return response if isinstance(response, bool) else False

    def create_task(self, task_req: TaskCreateReq) -> Task:
        """Create a new task.

        Args:
            task_req: Task creation request data.

        Returns:
            Created Task object.
        """
        response = self._request("POST", "/api/task/create", data=task_req)
        return Task.from_dict(response) if response else None

    def get_task_by_id(self, task_id: int) -> Task:
        """Get task by ID.

        Args:
            task_id: ID of the task to retrieve.

        Returns:
            Task object.
        """
        response = self._request("GET", f"/api/task/{task_id}")
        return Task.from_dict(response) if response else None

    def update_window_info(self, window_info_req: TaskUpdateWindowInfoReq) -> bool:
        """Update window information for a task.

        Args:
            window_info_req: Window info update request.

        Returns:
            True if update was successful, False otherwise.
        """
        response = self._request("POST", "/api/task/update/window-info", data=window_info_req)
        return response is not None

    def get_task_receive_list(self, list_req: TaskReceiveListReq) -> List[TaskReceiveListResp]:
        """Get list of tasks available for receiving.

        Args:
            list_req: Request parameters for filtering tasks.

        Returns:
            List of TaskReceiveListResp objects.
        """
        response = self._request("POST", "/api/task/receive/list", data=list_req)
        return [TaskReceiveListResp.from_dict(task) for task in response] if response else []

    def receive_task(self, receive_req: TaskReceiveReq) -> TaskReceiveResp:
        """Receive a task.

        Args:
            receive_req: Task receive request data.

        Returns:
            TaskReceiveResp object with task details.
        """
        response = self._request("POST", "/api/task/receive", data=receive_req)
        return TaskReceiveResp.from_dict(response) if response else None

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
