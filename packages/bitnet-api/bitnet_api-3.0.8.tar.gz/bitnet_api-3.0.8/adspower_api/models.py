from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class BaseResponse:
    """AdsPower API基础响应类"""
    code: int
    msg: str
    data: Optional[Any] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BaseResponse':
        """从API响应字典创建BaseResponse对象"""
        return cls(
            code=data.get('code', -1),
            msg=data.get('msg', ''),
            data=data.get('data')
        )


@dataclass
class BrowserFingerprint:
    """浏览器指纹配置"""
    automatic_timezone: Optional[str] = None
    timezone: Optional[str] = None
    webrtc: Optional[str] = None
    location: Optional[str] = None
    location_switch: Optional[str] = None
    longitude: Optional[str] = None
    latitude: Optional[str] = None
    accuracy: Optional[str] = None
    language: Optional[List[str]] = None
    language_switch: Optional[str] = None
    page_language_switch: Optional[str] = None
    page_language: Optional[str] = None
    ua: Optional[str] = None
    screen_resolution: Optional[str] = None
    fonts: Optional[List[str]] = None
    canvas: Optional[str] = None
    webgl_image: Optional[str] = None
    webgl: Optional[str] = None
    webgl_config: Optional[Dict] = None
    audio: Optional[str] = None
    do_not_track: Optional[str] = None
    hardware_concurrency: Optional[str] = None
    device_memory: Optional[str] = None
    flash: Optional[str] = None
    scan_port_type: Optional[str] = None
    allow_scan_ports: Optional[List[str]] = None
    media_devices: Optional[str] = None
    media_devices_num: Optional[Dict] = None
    client_rects: Optional[str] = None
    device_name_switch: Optional[str] = None
    device_name: Optional[str] = None
    random_ua: Optional[Dict] = None
    speech_switch: Optional[str] = None
    mac_address_config: Optional[Dict] = None
    browser_kernel_config: Optional[Dict] = None
    gpu: Optional[str] = None
    tls_switch: Optional[str] = None
    tls: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserFingerprint':
        """从API响应字典创建BrowserFingerprint对象"""
        if not data:
            return cls()
            
        return cls(
            automatic_timezone=data.get('automatic_timezone'),
            timezone=data.get('timezone'),
            webrtc=data.get('webrtc'),
            location=data.get('location'),
            location_switch=data.get('location_switch'),
            longitude=data.get('longitude'),
            latitude=data.get('latitude'),
            accuracy=data.get('accuracy'),
            language=data.get('language'),
            language_switch=data.get('language_switch'),
            page_language_switch=data.get('page_language_switch'),
            page_language=data.get('page_language'),
            ua=data.get('ua'),
            screen_resolution=data.get('screen_resolution'),
            fonts=data.get('fonts'),
            canvas=data.get('canvas'),
            webgl_image=data.get('webgl_image'),
            webgl=data.get('webgl'),
            webgl_config=data.get('webgl_config'),
            audio=data.get('audio'),
            do_not_track=data.get('do_not_track'),
            hardware_concurrency=data.get('hardware_concurrency'),
            device_memory=data.get('device_memory'),
            flash=data.get('flash'),
            scan_port_type=data.get('scan_port_type'),
            allow_scan_ports=data.get('allow_scan_ports'),
            media_devices=data.get('media_devices'),
            media_devices_num=data.get('media_devices_num'),
            client_rects=data.get('client_rects'),
            device_name_switch=data.get('device_name_switch'),
            device_name=data.get('device_name'),
            random_ua=data.get('random_ua'),
            speech_switch=data.get('speech_switch'),
            mac_address_config=data.get('mac_address_config'),
            browser_kernel_config=data.get('browser_kernel_config'),
            gpu=data.get('gpu'),
            tls_switch=data.get('tls_switch'),
            tls=data.get('tls')
        )
    
    def to_dict(self) -> Dict:
        """转换为API请求字典"""
        result = {}
        
        # 使用字典推导式简化代码
        attrs = [
            'automatic_timezone', 'timezone', 'webrtc', 'location', 'location_switch',
            'longitude', 'latitude', 'accuracy', 'language', 'language_switch',
            'page_language_switch', 'page_language', 'ua', 'screen_resolution',
            'fonts', 'canvas', 'webgl_image', 'webgl', 'webgl_config', 'audio',
            'do_not_track', 'hardware_concurrency', 'device_memory', 'flash',
            'scan_port_type', 'allow_scan_ports', 'media_devices', 'media_devices_num',
            'client_rects', 'device_name_switch', 'device_name', 'random_ua',
            'speech_switch', 'mac_address_config', 'browser_kernel_config', 'gpu',
            'tls_switch', 'tls'
        ]
        
        for attr in attrs:
            value = getattr(self, attr, None)
            if value is not None:
                result[attr] = value
                
        return result


@dataclass
class UserProxyConfig:
    """用户代理配置"""
    proxy_soft: Optional[str] = None  # 必需字段，代理软件类型
    proxy_type: Optional[str] = None
    proxy_host: Optional[str] = None
    proxy_port: Optional[str] = None
    proxy_user: Optional[str] = None
    proxy_password: Optional[str] = None
    proxy_url: Optional[str] = None  # 用于移动代理的URL
    global_config: Optional[str] = None  # 使用代理管理的账号列表信息
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'UserProxyConfig':
        """从API响应字典创建UserProxyConfig对象"""
        if not data:
            return cls()
            
        return cls(
            proxy_soft=data.get('proxy_soft'),
            proxy_type=data.get('proxy_type'),
            proxy_host=data.get('proxy_host'),
            proxy_port=data.get('proxy_port'),
            proxy_user=data.get('proxy_user'),
            proxy_password=data.get('proxy_password'),
            proxy_url=data.get('proxy_url'),
            global_config=data.get('global_config')
        )
    
    def to_dict(self) -> Dict:
        """转换为API请求字典"""
        result = {}
        
        # 使用字典推导式简化代码
        attrs = [
            'proxy_soft', 'proxy_type', 'proxy_host', 'proxy_port',
            'proxy_user', 'proxy_password', 'proxy_url', 'global_config'
        ]
        
        for attr in attrs:
            value = getattr(self, attr, None)
            if value is not None:
                result[attr] = value
                
        return result


@dataclass
class Browser:
    """浏览器环境详情"""
    profile_id: Optional[str] = None
    profile_no: Optional[str] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    platform: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    fakey: Optional[str] = None
    cookie: Optional[str] = None
    ip: Optional[str] = None
    ip_country: Optional[str] = None
    created_time: Optional[str] = None
    last_open_time: Optional[str] = None
    category_id: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Browser':
        """从API响应字典创建Browser对象"""
        return cls(
            profile_id=data.get('profile_id'),
            profile_no=data.get('profile_no'),
            name=data.get('name'),
            remark=data.get('remark'),
            group_id=data.get('group_id'),
            group_name=data.get('group_name'),
            platform=data.get('platform'),
            username=data.get('username'),
            password=data.get('password'),
            fakey=data.get('fakey'),
            cookie=data.get('cookie'),
            ip=data.get('ip'),
            ip_country=data.get('ip_country'),
            created_time=data.get('created_time'),
            last_open_time=data.get('last_open_time'),
            category_id=data.get('category_id')
        )


@dataclass
class Group:
    """分组信息"""
    group_id: Optional[str] = None
    group_name: Optional[str] = None
    remark: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Group':
        """从API响应字典创建Group对象"""
        return cls(
            group_id=data.get('group_id'),
            group_name=data.get('group_name'),
            remark=data.get('remark')
        )


@dataclass
class PageInfo:
    """分页信息"""
    page: int
    page_size: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PageInfo':
        """从API响应字典创建PageInfo对象"""
        return cls(
            page=data.get('page', 1),
            page_size=data.get('page_size', 1)
        )


@dataclass
class BrowserListResponse(BaseResponse):
    """浏览器列表响应"""
    browsers: List[Browser] = None
    page_info: Optional[PageInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserListResponse':
        """从API响应字典创建BrowserListResponse对象"""
        response = super().from_dict(data)
        
        browsers = []
        page_info = None
        
        if response.code == 0 and isinstance(response.data, dict):
            if 'list' in response.data and isinstance(response.data['list'], list):
                browsers = [Browser.from_dict(item) for item in response.data['list']]
            
            page_info = PageInfo.from_dict(response.data)
        
        return cls(
            code=response.code,
            msg=response.msg,
            data=response.data,
            browsers=browsers,
            page_info=page_info
        )


@dataclass
class GroupListResponse(BaseResponse):
    """分组列表响应"""
    groups: List[Group] = None
    page_info: Optional[PageInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GroupListResponse':
        """从API响应字典创建GroupListResponse对象"""
        response = super().from_dict(data)
        
        groups = []
        page_info = None
        
        if response.code == 0 and isinstance(response.data, dict):
            if 'list' in response.data and isinstance(response.data['list'], list):
                groups = [Group.from_dict(item) for item in response.data['list']]
            
            page_info = PageInfo.from_dict(response.data)
        
        return cls(
            code=response.code,
            msg=response.msg,
            data=response.data,
            groups=groups,
            page_info=page_info
        )


@dataclass
class BrowserResponse(BaseResponse):
    """单个浏览器响应"""
    browser: Optional[Browser] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserResponse':
        """从API响应字典创建BrowserResponse对象"""
        response = super().from_dict(data)
        browser = None
        
        if response.code == 0 and isinstance(response.data, dict):
            if 'profile_id' in response.data:
                browser = Browser.from_dict(response.data)
        
        return cls(
            code=response.code,
            msg=response.msg,
            data=response.data,
            browser=browser
        )


@dataclass
class BrowserActiveResponse(BaseResponse):
    """浏览器活动状态响应"""
    status: Optional[str] = None
    selenium: Optional[str] = None
    puppeteer: Optional[str] = None
    debug_port: Optional[str] = None
    webdriver: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserActiveResponse':
        """从API响应字典创建BrowserActiveResponse对象"""
        response = super().from_dict(data)
        
        status = None
        selenium = None
        puppeteer = None
        debug_port = None
        webdriver = None
        
        if response.code == 0 and isinstance(response.data, dict):
            status = response.data.get('status')
            debug_port = response.data.get('debug_port')
            webdriver = response.data.get('webdriver')
            
            if 'ws' in response.data and isinstance(response.data['ws'], dict):
                selenium = response.data['ws'].get('selenium')
                puppeteer = response.data['ws'].get('puppeteer')
        
        return cls(
            code=response.code,
            msg=response.msg,
            data=response.data,
            status=status,
            selenium=selenium,
            puppeteer=puppeteer,
            debug_port=debug_port,
            webdriver=webdriver
        )