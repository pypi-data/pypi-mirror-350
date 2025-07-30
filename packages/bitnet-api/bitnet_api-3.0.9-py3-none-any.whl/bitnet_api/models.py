from typing import List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class BaseResponse:
    """Base class for all API responses"""
    success: bool
    msg: Optional[str] = None


@dataclass
class BrowserCookie:
    """Browser cookie model"""
    name: str
    value: str
    domain: str
    path: str = "/"
    expires: Optional[int] = None
    http_only: bool = False
    secure: bool = False
    session: bool = False
    same_site: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserCookie':
        """Create a BrowserCookie object from dictionary"""
        return cls(
            name=data.get('name', ''),
            value=data.get('value', ''),
            domain=data.get('domain', ''),
            path=data.get('path', '/'),
            expires=data.get('expires'),
            http_only=data.get('httpOnly', False),
            secure=data.get('secure', False),
            session=data.get('session', False),
            same_site=data.get('sameSite')
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API requests"""
        result = {
            'name': self.name,
            'value': self.value,
            'domain': self.domain,
            'path': self.path
        }
        
        if self.expires is not None:
            result['expires'] = self.expires
        if self.http_only:
            result['httpOnly'] = self.http_only
        if self.secure:
            result['secure'] = self.secure
        if self.session:
            result['session'] = self.session
        if self.same_site:
            result['sameSite'] = self.same_site
            
        return result


@dataclass
class BrowserFingerPrint:
    """Browser fingerprint configuration"""
    # 基础参数
    core_version: Optional[str] = None
    core_product: Optional[str] = None
    os: Optional[str] = None
    os_version: Optional[str] = None
    ostype: Optional[str] = None
    version: Optional[str] = None
    user_agent: Optional[str] = None
    
    # 时区和位置
    is_ip_create_time_zone: Optional[bool] = None
    time_zone: Optional[str] = None
    time_zone_offset: Optional[int] = None
    is_ip_create_position: Optional[bool] = None
    lat: Optional[str] = None
    lng: Optional[str] = None
    precision_data: Optional[str] = None
    
    # 语言设置
    is_ip_create_language: Optional[bool] = None
    languages: Optional[str] = None
    is_ip_create_display_language: Optional[bool] = None
    display_languages: Optional[str] = None
    
    # 分辨率和窗口
    open_width: Optional[int] = None
    open_height: Optional[int] = None
    resolution_type: Optional[str] = None
    resolution: Optional[str] = None
    window_size_limit: Optional[bool] = None
    device_pixel_ratio: Optional[float] = None
    
    # 保护和隐私设置
    web_rtc: Optional[str] = None
    ignore_https_errors: Optional[bool] = None
    position: Optional[str] = None
    port_scan_protect: Optional[str] = None
    port_white_list: Optional[str] = None
    do_not_track: Optional[str] = None
    
    # 指纹防护
    font_type: Optional[str] = None
    canvas: Optional[str] = None
    web_gl: Optional[str] = None
    web_gl_meta: Optional[str] = None
    web_gl_manufacturer: Optional[str] = None
    web_gl_render: Optional[str] = None
    audio_context: Optional[str] = None
    media_device: Optional[str] = None
    speech_voices: Optional[str] = None
    hardware_concurrency: Optional[str] = None
    device_memory: Optional[str] = None
    client_rect_noise_enabled: Optional[bool] = None
    
    # 设备信息
    device_info_enabled: Optional[bool] = None
    computer_name: Optional[str] = None
    mac_addr: Optional[str] = None
    
    # SSL设置
    disable_ssl_cipher_suites_flag: Optional[bool] = None
    disable_ssl_cipher_suites: Optional[str] = None
    
    # 插件
    enable_plugins: Optional[bool] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserFingerPrint':
        """Create a BrowserFingerPrint object from API response dictionary"""
        if not data:
            return cls()
        
        return cls(
            core_version=data.get('coreVersion'),
            core_product=data.get('coreProduct'),
            os=data.get('os'),
            os_version=data.get('osVersion'),
            ostype=data.get('ostype'),
            version=data.get('version'),
            user_agent=data.get('userAgent'),
            
            is_ip_create_time_zone=data.get('isIpCreateTimeZone'),
            time_zone=data.get('timeZone'),
            time_zone_offset=data.get('timeZoneOffset'),
            is_ip_create_position=data.get('isIpCreatePosition'),
            lat=data.get('lat'),
            lng=data.get('lng'),
            precision_data=data.get('precisionData'),
            
            is_ip_create_language=data.get('isIpCreateLanguage'),
            languages=data.get('languages'),
            is_ip_create_display_language=data.get('isIpCreateDisplayLanguage'),
            display_languages=data.get('displayLanguages'),
            
            open_width=data.get('openWidth'),
            open_height=data.get('openHeight'),
            resolution_type=data.get('resolutionType'),
            resolution=data.get('resolution'),
            window_size_limit=data.get('windowSizeLimit'),
            device_pixel_ratio=data.get('devicePixelRatio'),
            
            web_rtc=data.get('webRTC'),
            ignore_https_errors=data.get('ignoreHttpsErrors'),
            position=data.get('position'),
            port_scan_protect=data.get('portScanProtect'),
            port_white_list=data.get('portWhiteList'),
            do_not_track=data.get('doNotTrack'),
            
            font_type=data.get('fontType'),
            canvas=data.get('canvas'),
            web_gl=data.get('webGL'),
            web_gl_meta=data.get('webGLMeta'),
            web_gl_manufacturer=data.get('webGLManufacturer'),
            web_gl_render=data.get('webGLRender'),
            audio_context=data.get('audioContext'),
            media_device=data.get('mediaDevice'),
            speech_voices=data.get('speechVoices'),
            hardware_concurrency=data.get('hardwareConcurrency'),
            device_memory=data.get('deviceMemory'),
            client_rect_noise_enabled=data.get('clientRectNoiseEnabled'),
            
            device_info_enabled=data.get('deviceInfoEnabled'),
            computer_name=data.get('computerName'),
            mac_addr=data.get('macAddr'),
            
            disable_ssl_cipher_suites_flag=data.get('disableSslCipherSuitesFlag'),
            disable_ssl_cipher_suites=data.get('disableSslCipherSuites'),
            
            enable_plugins=data.get('enablePlugins')
        )
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for API requests"""
        result = {}
        
        # 基础参数
        if self.core_version:
            result['coreVersion'] = self.core_version
        if self.core_product:
            result['coreProduct'] = self.core_product
        if self.os:
            result['os'] = self.os
        if self.os_version:
            result['osVersion'] = self.os_version
        if self.ostype:
            result['ostype'] = self.ostype
        if self.version:
            result['version'] = self.version
        if self.user_agent:
            result['userAgent'] = self.user_agent
        
        # 时区和位置
        if self.is_ip_create_time_zone is not None:
            result['isIpCreateTimeZone'] = self.is_ip_create_time_zone
        if self.time_zone:
            result['timeZone'] = self.time_zone
        if self.time_zone_offset is not None:
            result['timeZoneOffset'] = self.time_zone_offset
        if self.is_ip_create_position is not None:
            result['isIpCreatePosition'] = self.is_ip_create_position
        if self.lat:
            result['lat'] = self.lat
        if self.lng:
            result['lng'] = self.lng
        if self.precision_data:
            result['precisionData'] = self.precision_data
        
        # 语言设置
        if self.is_ip_create_language is not None:
            result['isIpCreateLanguage'] = self.is_ip_create_language
        if self.languages:
            result['languages'] = self.languages
        if self.is_ip_create_display_language is not None:
            result['isIpCreateDisplayLanguage'] = self.is_ip_create_display_language
        if self.display_languages:
            result['displayLanguages'] = self.display_languages
        
        # 分辨率和窗口
        if self.open_width is not None:
            result['openWidth'] = self.open_width
        if self.open_height is not None:
            result['openHeight'] = self.open_height
        if self.resolution_type:
            result['resolutionType'] = self.resolution_type
        if self.resolution:
            result['resolution'] = self.resolution
        if self.window_size_limit is not None:
            result['windowSizeLimit'] = self.window_size_limit
        if self.device_pixel_ratio is not None:
            result['devicePixelRatio'] = self.device_pixel_ratio
        
        # 保护和隐私设置
        if self.web_rtc:
            result['webRTC'] = self.web_rtc
        if self.ignore_https_errors is not None:
            result['ignoreHttpsErrors'] = self.ignore_https_errors
        if self.position:
            result['position'] = self.position
        if self.port_scan_protect:
            result['portScanProtect'] = self.port_scan_protect
        if self.port_white_list:
            result['portWhiteList'] = self.port_white_list
        if self.do_not_track:
            result['doNotTrack'] = self.do_not_track
        
        # 指纹防护
        if self.font_type:
            result['fontType'] = self.font_type
        if self.canvas:
            result['canvas'] = self.canvas
        if self.web_gl:
            result['webGL'] = self.web_gl
        if self.web_gl_meta:
            result['webGLMeta'] = self.web_gl_meta
        if self.web_gl_manufacturer:
            result['webGLManufacturer'] = self.web_gl_manufacturer
        if self.web_gl_render:
            result['webGLRender'] = self.web_gl_render
        if self.audio_context:
            result['audioContext'] = self.audio_context
        if self.media_device:
            result['mediaDevice'] = self.media_device
        if self.speech_voices:
            result['speechVoices'] = self.speech_voices
        if self.hardware_concurrency:
            result['hardwareConcurrency'] = self.hardware_concurrency
        if self.device_memory:
            result['deviceMemory'] = self.device_memory
        if self.client_rect_noise_enabled is not None:
            result['clientRectNoiseEnabled'] = self.client_rect_noise_enabled
        
        # 设备信息
        if self.device_info_enabled is not None:
            result['deviceInfoEnabled'] = self.device_info_enabled
        if self.computer_name:
            result['computerName'] = self.computer_name
        if self.mac_addr:
            result['macAddr'] = self.mac_addr
        
        # SSL设置
        if self.disable_ssl_cipher_suites_flag is not None:
            result['disableSslCipherSuitesFlag'] = self.disable_ssl_cipher_suites_flag
        if self.disable_ssl_cipher_suites:
            result['disableSslCipherSuites'] = self.disable_ssl_cipher_suites
        
        # 插件
        if self.enable_plugins is not None:
            result['enablePlugins'] = self.enable_plugins
            
        return result


@dataclass
class Browser:
    """Browser window details"""
    id: Optional[str] = None
    name: Optional[str] = None
    remark: Optional[str] = None
    seq: Optional[int] = None
    group_id: Optional[str] = None
    ws: Optional[str] = None
    http: Optional[str] = None
    core_version: Optional[str] = None
    pid: Optional[int] = None
    driver: Optional[str] = None  # chromedriver路径
    
    # 代理设置
    proxy_method: Optional[int] = None
    proxy_type: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
    proxy_user_name: Optional[str] = None
    proxy_password: Optional[str] = None
    refresh_proxy_url: Optional[str] = None
    is_ipv6: Optional[bool] = None
    ip_check_service: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    
    # 动态IP设置
    dynamic_ip_url: Optional[str] = None
    dynamic_ip_channel: Optional[str] = None
    is_dynamic_ip_change_ip: Optional[bool] = None
    duplicate_check: Optional[int] = None
    
    # 平台信息
    platform: Optional[str] = None
    url: Optional[str] = None
    user_name: Optional[str] = None
    password: Optional[str] = None
    is_syn_open: Optional[bool] = None
    fa_secret_key: Optional[str] = None
    cookie: Optional[str] = None
    
    # 浏览器设置
    workbench: Optional[str] = None
    abort_image: Optional[bool] = None
    abort_image_max_size: Optional[int] = None
    abort_media: Optional[bool] = None
    mute_audio: Optional[bool] = None
    stop_while_net_error: Optional[bool] = None
    stop_while_ip_change: Optional[bool] = None
    stop_while_country_change: Optional[bool] = None
    
    # 指纹信息
    browser_finger_print: Optional[BrowserFingerPrint] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Browser':
        """Create a Browser object from API response dictionary"""
        browser_finger_print = None
        if 'browserFingerPrint' in data:
            browser_finger_print = BrowserFingerPrint.from_dict(data['browserFingerPrint'])
            
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            remark=data.get('remark'),
            seq=data.get('seq'),
            group_id=data.get('groupId'),
            ws=data.get('ws'),
            http=data.get('http'),
            core_version=data.get('coreVersion'),
            pid=data.get('pid'),
            driver=data.get('driver'),
            
            # 代理设置
            proxy_method=data.get('proxyMethod'),
            proxy_type=data.get('proxyType'),
            host=data.get('host'),
            port=data.get('port'),
            proxy_user_name=data.get('proxyUserName'),
            proxy_password=data.get('proxyPassword'),
            refresh_proxy_url=data.get('refreshProxyUrl'),
            is_ipv6=data.get('isIpv6'),
            ip_check_service=data.get('ipCheckService'),
            country=data.get('country'),
            province=data.get('province'),
            city=data.get('city'),
            
            # 动态IP设置
            dynamic_ip_url=data.get('dynamicIpUrl'),
            dynamic_ip_channel=data.get('dynamicIpChannel'),
            is_dynamic_ip_change_ip=data.get('isDynamicIpChangeIp'),
            duplicate_check=data.get('duplicateCheck'),
            
            # 平台信息
            platform=data.get('platform'),
            url=data.get('url'),
            user_name=data.get('userName'),
            password=data.get('password'),
            is_syn_open=data.get('isSynOpen'),
            fa_secret_key=data.get('faSecretKey'),
            cookie=data.get('cookie'),
            
            # 浏览器设置
            workbench=data.get('workbench'),
            abort_image=data.get('abortImage'),
            abort_image_max_size=data.get('abortImageMaxSize'),
            abort_media=data.get('abortMedia'),
            mute_audio=data.get('muteAudio'),
            stop_while_net_error=data.get('stopWhileNetError'),
            stop_while_ip_change=data.get('stopWhileIpChange'),
            stop_while_country_change=data.get('stopWhileCountryChange'),
            
            browser_finger_print=browser_finger_print
        )


@dataclass
class Group:
    """Browser group details"""
    id: str
    group_name: str
    sort_num: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Group':
        """Create a Group object from API response dictionary"""
        return cls(
            id=data['id'],
            group_name=data.get('groupName', ''),
            sort_num=data.get('sortNum', 0)
        )


@dataclass
class PageInfo:
    """Pagination information"""
    total_elements: int
    total_pages: int
    number: int
    size: int
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'PageInfo':
        """Create a PageInfo object from API response dictionary"""
        return cls(
            total_elements=data.get('totalElements', 0),
            total_pages=data.get('totalPages', 0),
            number=data.get('number', 0),
            size=data.get('size', 0)
        )


@dataclass
class PagedResult(BaseResponse):
    """Base class for paged results"""
    page_info: Optional[PageInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict, content_type, content_key: str = 'content') -> 'PagedResult':
        """Create a PagedResult object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        
        result = cls(success=success, msg=msg)
        
        if 'data' in data and isinstance(data['data'], dict):
            if content_key in data['data']:
                result.content = [content_type.from_dict(item) for item in data['data'][content_key]]
            
            # Extract pagination info if available
            if all(key in data['data'] for key in ['totalElements', 'totalPages', 'number', 'size']):
                result.page_info = PageInfo.from_dict(data['data'])
        
        return result


@dataclass
class BrowserListResponse(PagedResult):
    """Response for browser list API"""
    content: List[Browser] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserListResponse':
        """Create a BrowserListResponse object from API response dictionary"""
        result = super().from_dict(data, Browser, 'content')
        if result.content is None:
            result.content = []
        return result


@dataclass
class GroupListResponse(PagedResult):
    """Response for group list API"""
    content: List[Group] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GroupListResponse':
        """Create a GroupListResponse object from API response dictionary"""
        result = super().from_dict(data, Group, 'content')
        if result.content is None:
            result.content = []
        return result


@dataclass
class HealthResponse(BaseResponse):
    """Response for health check API"""
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'HealthResponse':
        """Create a HealthResponse object from API response dictionary"""
        return cls(
            success=data.get('success', False),
            msg=data.get('msg')
        )


@dataclass
class BrowserResponse(BaseResponse):
    """Response containing a single browser"""
    data: Optional[Browser] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserResponse':
        """Create a BrowserResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        browser_data = None
        # print(f'BrowserResponse raw: {data}')
        
        if success and 'data' in data and isinstance(data['data'], dict):
            browser_data = Browser.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=browser_data)


@dataclass
class GroupResponse(BaseResponse):
    """Response containing a single group"""
    data: Optional[Group] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GroupResponse':
        """Create a GroupResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        group_data = None
        
        if success and 'data' in data and isinstance(data['data'], dict):
            if 'id' in data['data']:
                group_data = Group.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=group_data)


@dataclass
class ProxyCheckInfo:
    """Proxy check information"""
    ip: str
    country_name: str
    state_prov: str
    country_code: str
    region: str
    city: str
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyCheckInfo':
        """Create a ProxyCheckInfo object from API response dictionary"""
        return cls(
            ip=data.get('ip', ''),
            country_name=data.get('countryName', ''),
            state_prov=data.get('stateProv', ''),
            country_code=data.get('countryCode', ''),
            region=data.get('region', ''),
            city=data.get('city', '')
        )


@dataclass
class ProxyCheckResponse(BaseResponse):
    """Response for proxy check API"""
    data: Optional[ProxyCheckInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'ProxyCheckResponse':
        """Create a ProxyCheckResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        proxy_data = None
        
        if success and 'data' in data:
            if isinstance(data['data'], dict):
                if data['data'].get('success') and 'data' in data['data']:
                    proxy_data = ProxyCheckInfo.from_dict(data['data']['data'])
        
        return cls(success=success, msg=msg, data=proxy_data)


@dataclass
class BrowserPidInfo:
    """Browser PID information"""
    browser_ids: Dict[str, str]  # Maps browser_id to PID
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserPidInfo':
        """Create a BrowserPidInfo object from API response dictionary"""
        return cls(browser_ids=data or {})


@dataclass
class BrowserPidResponse(BaseResponse):
    """Response for browser PID API"""
    data: Optional[BrowserPidInfo] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BrowserPidResponse':
        """Create a BrowserPidResponse object from API response dictionary"""
        success = data.get('success', False)
        msg = data.get('msg')
        pid_data = None
        
        if success and 'data' in data:
            pid_data = BrowserPidInfo.from_dict(data['data'])
        
        return cls(success=success, msg=msg, data=pid_data)


@dataclass
class GenericResponse(BaseResponse):
    """Generic response for API calls that don't return specific data"""
    data: Any = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'GenericResponse':
        """Create a GenericResponse object from API response dictionary"""
        return cls(
            success=data.get('success', False),
            msg=data.get('msg'),
            data=data.get('data')
        ) 