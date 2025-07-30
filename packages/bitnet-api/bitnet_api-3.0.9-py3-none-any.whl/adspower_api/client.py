import requests
from typing import Dict, List, Optional, Any, Union

from .models import (
    BaseResponse, BrowserResponse, BrowserListResponse, 
    GroupListResponse, BrowserActiveResponse, BrowserFingerprint,
    UserProxyConfig
)


class AdsPowerClient:
    """AdsPower API客户端"""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 50325):
        """初始化AdsPower API客户端
        
        Args:
            host: API主机地址
            port: API端口号
        """
        self.base_url = f"http://{host}:{port}"
        self.headers = {"Content-Type": "application/json"}
    
    def _post(self, endpoint: str, data: Dict = None) -> Dict:
        """发送POST请求到API
        
        Args:
            endpoint: API端点（不带前导斜杠）
            data: 请求数据（将转换为JSON）
            
        Returns:
            响应数据字典
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data or {})
        response.raise_for_status()
        return response.json()
    
    def _get(self, endpoint: str, params: Dict = None) -> Dict:
        """发送GET请求到API
        
        Args:
            endpoint: API端点（不带前导斜杠）
            params: 请求参数
            
        Returns:
            响应数据字典
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        response.raise_for_status()
        return response.json()
    
    # 浏览器环境管理API
    def create_browser(self, 
                      group_id: str,
                      name: Optional[str] = None,
                      remark: Optional[str] = None,
                      platform: Optional[str] = None,
                      username: Optional[str] = None,
                      password: Optional[str] = None,
                      fakey: Optional[str] = None,
                      cookie: Optional[str] = None,
                      repeat_config: Optional[List[int]] = None,
                      ignore_cookie_error: Optional[str] = None,
                      tabs: Optional[List[str]] = None,
                      user_proxy_config: Optional[Union[Dict, UserProxyConfig]] = None,
                      proxyid: Optional[str] = None,
                      ip: Optional[str] = None,
                      country: Optional[str] = None,
                      region: Optional[str] = None,
                      city: Optional[str] = None,
                      ipchecker: Optional[str] = None,
                      fingerprint_config: Optional[Union[Dict, BrowserFingerprint]] = None,
                      category_id: Optional[str] = None) -> BrowserResponse:
        """创建新的浏览器环境
        
        Args:
            group_id: 分组ID
            name: 浏览器名称
            remark: 备注
            platform: 账号平台域名
            username: 账号用户名
            password: 账号密码
            fakey: 2FA密钥
            cookie: 账号Cookie
            repeat_config: 账号去重配置
            ignore_cookie_error: Cookie校验失败处理方式
            tabs: 标签页URL列表
            user_proxy_config: 环境代理配置
            proxyid: 代理ID
            ip: 代理IP
            country: 代理国家/地区
            region: 代理州/省
            city: 代理城市
            ipchecker: IP查询渠道
            fingerprint_config: 指纹配置
            category_id: 应用分类ID
            
        Returns:
            BrowserResponse对象
        """
        # 转换UserProxyConfig为字典
        if isinstance(user_proxy_config, UserProxyConfig):
            user_proxy_config = user_proxy_config.to_dict()
            
        # 转换BrowserFingerprint为字典
        if isinstance(fingerprint_config, BrowserFingerprint):
            fingerprint_config = fingerprint_config.to_dict()
        elif fingerprint_config is None:
            # 提供默认指纹配置
            fingerprint_config = {"automatic_timezone": "1"}
            
        data = {
            "group_id": group_id,
            "name": name,
            "remark": remark,
            "platform": platform,
            "username": username,
            "password": password,
            "fakey": fakey,
            "cookie": cookie,
            "repeat_config": repeat_config,
            "ignore_cookie_error": ignore_cookie_error,
            "tabs": tabs,
            "user_proxy_config": user_proxy_config,
            "proxyid": proxyid,
            "ip": ip,
            "country": country,
            "region": region,
            "city": city,
            "ipchecker": ipchecker,
            "fingerprint_config": fingerprint_config,
            "category_id": category_id
        }
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        # api/v2/browser-profile/create
        response_data = self._post("api/v2/browser-profile/create", data)
        return BrowserResponse.from_dict(response_data)
    
    def start_browser(self, 
                     profile_id: Optional[str] = None,
                     profile_no: Optional[str] = None,
                     launch_args: Optional[List[str]] = None,
                     headless: Optional[str] = None,
                     last_opened_tabs: Optional[str] = None,
                     proxy_detection: Optional[str] = None,
                     password_filling: Optional[str] = None,
                     password_saving: Optional[str] = None,
                     cdp_mask: Optional[str] = None,
                     delete_cache: Optional[str] = None,
                     device_scale: Optional[str] = None) -> BrowserActiveResponse:
        """启动浏览器
        
        Args:
            profile_id: 环境ID
            profile_no: 环境编号
            launch_args: 启动参数
            headless: 是否启动headless浏览器
            last_opened_tabs: 是否继续浏览上次打开的标签页
            proxy_detection: 是否打开检测页面
            password_filling: 是否启用填充账密功能
            password_saving: 是否允许保存密码
            cdp_mask: 是否屏蔽CDP检测
            delete_cache: 是否在关闭浏览器后清除缓存
            device_scale: 手机模式下的缩放比
            
        Returns:
            BrowserResponse对象
        """
        data = {}
        if profile_id:
            data["profile_id"] = profile_id
        if profile_no:
            data["profile_no"] = profile_no
        if launch_args:
            data["launch_args"] = launch_args
        if headless:
            data["headless"] = headless
        if last_opened_tabs:
            data["last_opened_tabs"] = last_opened_tabs
        if proxy_detection:
            data["proxy_detection"] = proxy_detection
        if password_filling:
            data["password_filling"] = password_filling
        if password_saving:
            data["password_saving"] = password_saving
        if cdp_mask:
            data["cdp_mask"] = cdp_mask
        if delete_cache:
            data["delete_cache"] = delete_cache
        if device_scale:
            data["device_scale"] = device_scale
            
        response_data = self._post("api/v2/browser-profile/start", data)
        print(f'start response_data:{response_data}')
        return BrowserActiveResponse.from_dict(response_data)
    
    def stop_browser(self, profile_id: Optional[str] = None, profile_no: Optional[str] = None) -> BaseResponse:
        """关闭浏览器
        
        Args:
            profile_id: 环境ID
            profile_no: 环境编号
            
        Returns:
            BaseResponse对象
        """
        data = {}
        if profile_id:
            data["profile_id"] = profile_id
        if profile_no:
            data["profile_no"] = profile_no
            
        response_data = self._post("api/v2/browser-profile/stop", data)
        return BaseResponse.from_dict(response_data)
    
    def list_browsers(self, 
                      group_id: Optional[str] = None,
                      profile_id: Optional[List[str]] = None,
                      profile_no: Optional[List[str]] = None,
                      sort_type: Optional[str] = None,
                      sort_order: Optional[str] = None,
                      page: int = 1,
                      limit: int = 50) -> BrowserListResponse:
        """查询环境列表
        
        Args:
            group_id: 分组ID
            profile_id: 环境ID列表
            profile_no: 环境编号列表
            sort_type: 排序类型
            sort_order: 排序顺序
            page: 页码
            limit: 每页数量
            
        Returns:
            BrowserListResponse对象
        """
        data = {
            "page": page,
            "limit": limit
        }
        
        if group_id:
            data["group_id"] = group_id
        if profile_id:
            data["profile_id"] = profile_id
        if profile_no:
            data["profile_no"] = profile_no
        if sort_type:
            data["sort_type"] = sort_type
        if sort_order:
            data["sort_order"] = sort_order
            
        response_data = self._post("api/v2/browser-profile/list", data)
        return BrowserListResponse.from_dict(response_data)
    
    def update_browser(self, 
                       profile_id: str,
                       name: Optional[str] = None,
                       remark: Optional[str] = None,
                       platform: Optional[str] = None,
                       username: Optional[str] = None,
                       password: Optional[str] = None,
                       fakey: Optional[str] = None,
                       cookie: Optional[str] = None,
                       ignore_cookie_error: Optional[str] = None,
                       tabs: Optional[List[str]] = None,
                       user_proxy_config: Optional[Union[Dict, UserProxyConfig]] = None,
                       proxyid: Optional[str] = None,
                       ip: Optional[str] = None,
                       country: Optional[str] = None,
                       region: Optional[str] = None,
                       city: Optional[str] = None,
                       fingerprint_config: Optional[Union[Dict, BrowserFingerprint]] = None,
                       category_id: Optional[str] = None,
                       launch_args: Optional[List[str]] = None) -> BaseResponse:
        """更新浏览器环境
        
        Args:
            profile_id: 环境ID
            name: 浏览器名称
            remark: 备注
            platform: 账号平台域名
            username: 账号用户名
            password: 账号密码
            fakey: 2FA密钥
            cookie: 账号Cookie
            ignore_cookie_error: Cookie校验失败处理方式
            tabs: 标签页URL列表
            user_proxy_config: 环境代理配置
            proxyid: 代理ID
            ip: 代理IP
            country: 代理国家/地区
            region: 代理州/省
            city: 代理城市
            fingerprint_config: 指纹配置
            category_id: 应用分类ID
            launch_args: 启动参数
            
        Returns:
            BaseResponse对象
        """
        # 转换UserProxyConfig为字典
        if isinstance(user_proxy_config, UserProxyConfig):
            user_proxy_config = user_proxy_config.to_dict()
            
        # 转换BrowserFingerprint为字典
        if isinstance(fingerprint_config, BrowserFingerprint):
            fingerprint_config = fingerprint_config.to_dict()
            
        data = {
            "profile_id": profile_id,
            "name": name,
            "remark": remark,
            "platform": platform,
            "username": username,
            "password": password,
            "fakey": fakey,
            "cookie": cookie,
            "ignore_cookie_error": ignore_cookie_error,
            "tabs": tabs,
            "user_proxy_config": user_proxy_config,
            "proxyid": proxyid,
            "ip": ip,
            "country": country,
            "region": region,
            "city": city,
            "fingerprint_config": fingerprint_config,
            "category_id": category_id,
            "launch_args": launch_args
        }
        
        # 移除None值
        data = {k: v for k, v in data.items() if v is not None}
        
        response_data = self._post("api/v2/browser-profile/update", data)
        return BaseResponse.from_dict(response_data)
    
    def delete_browser(self, profile_id: List[str]) -> BaseResponse:
        """删除浏览器环境
        
        Args:
            profile_id: 环境ID列表
            
        Returns:
            BaseResponse对象
        """
        data = {"profile_id": profile_id}
        response_data = self._post("api/v2/browser-profile/delete", data)
        return BaseResponse.from_dict(response_data)
    
    def check_browser_active(self, profile_id: Optional[str] = None, profile_no: Optional[str] = None) -> BrowserActiveResponse:
        """检查浏览器活动状态
        
        Args:
            profile_id: 环境ID
            profile_no: 环境编号
            
        Returns:
            BrowserActiveResponse对象
        """
        params = {}
        if profile_id:
            params["profile_id"] = profile_id
        if profile_no:
            params["profile_no"] = profile_no
            
        response_data = self._get("api/v2/browser-profile/active", params)
        return BrowserActiveResponse.from_dict(response_data)
    
    def list_groups(self, group_name: Optional[str] = None, page: int = 1, page_size: int = 10) -> GroupListResponse:
        """查询分组列表
        
        Args:
            group_name: 分组名称
            page: 页码
            page_size: 每页数量
            
        Returns:
            GroupListResponse对象
        """
        params = {
            "page": page,
            "page_size": page_size
        }
        
        if group_name:
            params["group_name"] = group_name
            
        response_data = self._get("api/v1/group/list", params)
        return GroupListResponse.from_dict(response_data)
    
    def check_status(self) -> BaseResponse:
        """检查API接口状态
        
        用于检查当前设备API接口的可用性。
        
        Returns:
            BaseResponse对象，code为0表示API可用
        """
        response_data = self._get("status")
        return BaseResponse.from_dict(response_data)