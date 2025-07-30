"""
FlyWing API Models

This module defines the data models used in the FlyWing API client.
"""

import re
from dataclasses import dataclass, field, fields, asdict
from typing import List, Dict, Any, Optional, TypeVar, Type, ClassVar, get_type_hints, get_origin, get_args, Union
from datetime import datetime


def camel_to_snake(name: str) -> str:
    """
    Convert camelCase string to snake_case.
    
    Args:
        name: A string in camelCase format.
        
    Returns:
        The string converted to snake_case.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_to_camel(name: str) -> str:
    """
    Convert snake_case string to camelCase.
    
    Args:
        name: A string in snake_case format.
        
    Returns:
        The string converted to camelCase.
    """
    components = name.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


T = TypeVar('T', bound='BaseModel')

@dataclass
class BaseModel:
    """Base model with dictionary conversion methods."""
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """
        Create a model instance from a dictionary.
        Handles camelCase to snake_case conversion and nested models.
        
        Args:
            data: Dictionary containing model data with camelCase keys.
            
        Returns:
            An instance of the model.
        """
        if data is None:
            return None
            
        # Convert camelCase keys to snake_case
        snake_case_data = {}
        for key, value in data.items():
            snake_case_data[camel_to_snake(key)] = value
            
        # Get type hints for the class
        type_hints = get_type_hints(cls)
        init_kwargs = {}
        
        # Process each field
        for field_name, field_type in type_hints.items():
            # Skip ClassVar fields
            if get_origin(field_type) is ClassVar:
                continue
                
            # If field is not in data, skip it
            if field_name not in snake_case_data:
                continue
                
            value = snake_case_data[field_name]
            
            # Handle None values
            if value is None:
                init_kwargs[field_name] = None
                continue
                
            # Handle nested dataclass
            origin = get_origin(field_type)
            args = get_args(field_type)
            
            # Handle Optional types
            if origin is Union and type(None) in args:
                # Extract the actual type from Optional
                inner_types = [arg for arg in args if arg is not type(None)]
                if inner_types:
                    field_type = inner_types[0]
                    origin = get_origin(field_type)
                    args = get_args(field_type)
            
            # Handle List
            if origin is list and args and hasattr(args[0], 'from_dict') and value:
                init_kwargs[field_name] = [args[0].from_dict(item) for item in value]
            # Handle nested dataclass
            elif hasattr(field_type, 'from_dict') and value:
                init_kwargs[field_name] = field_type.from_dict(value)
            # Handle datetime
            elif field_type is datetime and isinstance(value, str):
                init_kwargs[field_name] = datetime.fromisoformat(value.replace('Z', '+00:00'))
            # Handle other types
            else:
                init_kwargs[field_name] = value
                
        return cls(**init_kwargs)
        
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary with camelCase keys.
        Handles nested models and datetime objects.
        
        Returns:
            Dictionary representation of the model with camelCase keys.
        """
        result = {}
        data = asdict(self)
        
        for key, value in data.items():
            # Handle None values
            if value is None:
                result[snake_to_camel(key)] = None
                continue
                
            # Handle nested dataclass
            if hasattr(value, 'to_dict'):
                result[snake_to_camel(key)] = value.to_dict()
            # Handle list of dataclasses
            elif isinstance(value, list) and value and hasattr(value[0], 'to_dict'):
                result[snake_to_camel(key)] = [item.to_dict() for item in value]
            # Handle datetime
            elif isinstance(value, datetime):
                result[snake_to_camel(key)] = value.isoformat()
            # Handle other types
            else:
                result[snake_to_camel(key)] = value
                
        return result


@dataclass
class ProxyInfo(BaseModel):
    """Proxy information model."""
    host: str
    port: str
    user: str
    password: str
    proxy_method: str


@dataclass
class ProxyConfig(BaseModel):
    """Proxy configuration model."""
    id: Optional[int] = None
    proxy_name: Optional[str] = None
    proxy_type: Optional[str] = None
    account: Optional[str] = None
    api_url: Optional[str] = None
    balance: Optional[float] = None
    valid_time: Optional[int] = None
    status: Optional[bool] = None


@dataclass
class Domain(BaseModel):
    """Domain information model."""
    id: Optional[int] = None
    domain: Optional[str] = None
    ip: Optional[str] = None
    country_code: Optional[str] = None
    country_name: Optional[str] = None
    use_count: Optional[int] = None


@dataclass
class Task(BaseModel):
    """Task model."""
    id: Optional[int] = None
    task_name: Optional[str] = None
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    description: Optional[str] = None
    proxy_config_id: Optional[int] = None
    proxy_config_name: Optional[str] = None
    open_url: Optional[str] = None
    window_count: Optional[int] = None
    start_time: Optional[datetime] = None
    status: Optional[str] = None
    auto_cookie: Optional[bool] = None


@dataclass
class TaskCheckReq(BaseModel):
    """Task check request model."""
    group_id: str
    task_name: str


@dataclass
class TaskDetailCreateReq(BaseModel):
    """Task detail creation request model."""
    window_info_json: str


@dataclass
class TaskCreateReq(BaseModel):
    """Task creation request model."""
    group_id: str
    group_name: str
    task_name: str
    open_url: str
    proxy_config_id: int
    proxy_config_name: str
    window_count: int
    start_time: datetime
    task_detail_list: List[TaskDetailCreateReq]


@dataclass
class TaskReceiveListReq(BaseModel):
    """Task receive list request model."""
    browser_id: Optional[str] = None
    group_id: Optional[str] = None


@dataclass
class TaskReceiveListResp(BaseModel):
    """Task receive list response model."""
    task_id: Optional[int] = None
    task_detail_id: Optional[int] = None
    browser_id: Optional[str] = None
    browser_name: Optional[str] = None
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    task_name: Optional[str] = None
    cst_time_range: Optional[str] = None
    os: Optional[str] = None
    proxy_config_id: Optional[int] = None
    proxy_valid_time: Optional[int] = None
    seq: Optional[int] = None
    task_start_hour: Optional[int] = None
    task_end_hour: Optional[int] = None
    task_status: Optional[str] = None
    task_status_name: Optional[str] = None


@dataclass
class TaskReceiveReq(BaseModel):
    """Task receive request model."""
    browser_id: Optional[str] = None
    browser_name: Optional[str] = None
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    task_id: Optional[int] = None
    task_name: Optional[str] = None
    task_detail_id: Optional[int] = None
    cst_time_range: Optional[str] = None
    os: Optional[str] = None
    proxy_config_id: Optional[int] = None
    proxy_valid_time: Optional[int] = None
    seq: Optional[int] = None
    task_start_hour: Optional[int] = None
    task_end_hour: Optional[int] = None
    task_status: Optional[str] = None
    task_status_name: Optional[str] = None


@dataclass
class TaskReceiveResp(BaseModel):
    """Task receive response model."""
    task_id: Optional[int] = None
    task_detail_id: Optional[int] = None
    browser_id: Optional[str] = None
    ad_domain: Optional[str] = None
    proxy_info: Optional[ProxyInfo] = None
    domains: Optional[List[Domain]] = None


@dataclass
class TaskUpdateWindowInfoReq(BaseModel):
    """Task update window info request model."""
    id: Optional[int] = None
    window_info_json: Optional[Dict[str, Any]] = None


@dataclass
class WorkingTime(BaseModel):
    """Working time model."""
    id: Optional[int] = None
    cst: Optional[str] = None
    est: Optional[str] = None
    pst: Optional[str] = None
    ratio: Optional[float] = None
    shift: Optional[int] = None
    status: Optional[bool] = None


@dataclass
class UserRegisterReq(BaseModel):
    """User register request model."""
    user_name: str
    password: str
    repeat_password: str
    mac_id: str
    device_info: Optional[str] = None


@dataclass
class ClientUser(BaseModel):
    """Client user model."""
    id: Optional[int] = None
    username: Optional[str] = None
    password: Optional[str] = None
    mac_id: Optional[str] = None
    device_info: Optional[str] = None
    change_mac_id_count: Optional[int] = None
    is_admin: Optional[bool] = None
    status: Optional[bool] = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None


@dataclass
class UserLoginResp(BaseModel):
    """User login response model."""
    token: Optional[str] = None
    client_user: Optional[ClientUser] = None


@dataclass
class AutoTask(BaseModel):
    """Auto task model."""
    id: Optional[int] = None
    task_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    create_date: Optional[datetime] = None
    update_date: Optional[datetime] = None


@dataclass
class AutoTaskLog(BaseModel):
    """Auto task log model."""
    id: Optional[int] = None
    task_id: Optional[int] = None
    log_content: Optional[str] = None
    status: Optional[str] = None
    create_date: Optional[datetime] = None


@dataclass
class AutoTaskUpdateResp(BaseModel):
    """Auto task update response model."""
    id: Optional[int] = None
    task_id: Optional[int] = None
    status: Optional[str] = None
    message: Optional[str] = None

