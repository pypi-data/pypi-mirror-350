import json
import requests
from typing import Dict, List, Optional, Union, Any

from .models import (
    HealthResponse, BrowserResponse, BrowserListResponse, 
    GroupResponse, GroupListResponse, ProxyCheckResponse, 
    BrowserPidResponse, GenericResponse, BrowserFingerPrint
)


class BitnetClient:
    """
    Client for interacting with the Bitnet Browser API
    """
    
    def __init__(self, host: str = "127.0.0.1", port: int = 54345, token: Optional[str] = None):
        """
        Initialize the Bitnet API client.
        
        Args:
            host: API host address
            port: API port number
            token: Authentication token (if required)
        """
        self.base_url = f"http://{host}:{port}"
        self.token = token
        self.headers = {
            "Content-Type": "application/json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"
    
    def _make_request(self, endpoint: str, data: Dict = None) -> Dict:
        """
        Make a POST request to the API.
        
        Args:
            endpoint: API endpoint (without leading slash)
            data: Request data (will be converted to JSON)
            
        Returns:
            Response data as dictionary
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=self.headers, json=data or {})
        response.raise_for_status()
        return response.json()
    
    # Health check API
    def health_check(self) -> HealthResponse:
        """Check if the API is running properly"""
        response_data = self._make_request("health")
        return HealthResponse.from_dict(response_data)
    
    # Browser management APIs
    def create_or_update_browser(self, 
                                id: Optional[str] = None,
                                group_id: Optional[str] = None,
                                name: Optional[str] = None,
                                remark: Optional[str] = None,
                                platform: Optional[str] = None,
                                url: Optional[str] = None,
                                user_name: Optional[str] = None,
                                password: Optional[str] = None,
                                is_syn_open: Optional[bool] = None,
                                fa_secret_key: Optional[str] = None,
                                cookie: Optional[str] = None,
                                
                                # 代理设置
                                proxy_method: int = 2,
                                proxy_type: str = "noproxy",
                                host: str = "",
                                port: str = "",
                                proxy_username: str = "",
                                proxy_password: str = "",
                                ip_check_service: Optional[str] = None,
                                is_ipv6: Optional[bool] = None,
                                refresh_proxy_url: Optional[str] = None,
                                country: Optional[str] = None,
                                province: Optional[str] = None,
                                city: Optional[str] = None,
                                
                                # 动态IP设置
                                dynamic_ip_url: Optional[str] = None,
                                dynamic_ip_channel: Optional[str] = None,
                                is_dynamic_ip_change_ip: Optional[bool] = None,
                                duplicate_check: Optional[int] = None,
                                
                                # 浏览器设置
                                workbench: Optional[str] = None,
                                abort_image: Optional[bool] = None,
                                abort_image_max_size: Optional[int] = None,
                                abort_media: Optional[bool] = None,
                                mute_audio: Optional[bool] = None,
                                stop_while_net_error: Optional[bool] = None,
                                stop_while_ip_change: Optional[bool] = None,
                                stop_while_country_change: Optional[bool] = None,
                                
                                # 指纹配置
                                browser_fingerprint: Optional[Union[Dict, BrowserFingerPrint]] = None) -> BrowserResponse:
        """
        Create a new browser window or update an existing one.
        
        Args:
            id: Browser ID (None for creating new browser)
            group_id: Group ID for the browser
            name: Browser name
            remark: Browser remark/description
            platform: Account platform URL (e.g., "https://www.facebook.com")
            url: Additional URLs to open, multiple separated by commas
            user_name: Platform account username for autofill
            password: Platform account password for autofill
            is_syn_open: Allow multiple accounts to open in the same browser window
            fa_secret_key: 2FA secret key
            cookie: Platform account cookie as JSON string
            
            # Proxy settings
            proxy_method: Proxy method to use (2=custom, 3=extract IP)
            proxy_type: Type of proxy (noproxy, http, socks5, etc.)
            host: Proxy host
            port: Proxy port
            proxy_username: Proxy authentication username
            proxy_password: Proxy authentication password
            ip_check_service: IP info service, options: "ip api", "ip123in", "luminati"
            is_ipv6: Whether it's IPv6 protocol
            refresh_proxy_url: Proxy refresh URL
            country: Country code for dynamic proxy
            province: Province/state code for dynamic proxy
            city: City code for dynamic proxy
            
            # Dynamic IP settings
            dynamic_ip_url: Extract IP URL for proxy_method=3
            dynamic_ip_channel: Extract IP service provider (rola, doveip, cloudam, common)
            is_dynamic_ip_change_ip: Whether to extract new IP for each browser open
            duplicate_check: Check for duplicate IPs (1=check, 0=don't check)
            
            # Browser settings
            workbench: Browser workbench page, "localserver" or "disable"
            abort_image: Block image loading
            abort_image_max_size: Block images larger than this size (in KB)
            abort_media: Block video autoplay
            mute_audio: Mute browser audio
            stop_while_net_error: Stop opening if network is unavailable
            stop_while_ip_change: Stop opening if IP changes
            stop_while_country_change: Stop opening if IP country changes
            
            # Fingerprint settings
            browser_fingerprint: Browser fingerprint configuration (dict or BrowserFingerPrint)
        
        Returns:
            BrowserResponse object with browser data
        """
        # Convert BrowserFingerPrint to dict if needed
        if isinstance(browser_fingerprint, BrowserFingerPrint):
            browser_fingerprint = browser_fingerprint.to_dict()
        elif browser_fingerprint is None:
            browser_fingerprint = {"coreVersion": "104"}
            
        data = {
            "id": id,
            "groupId": group_id,
            "name": name,
            "remark": remark,
            "platform": platform,
            "url": url,
            "userName": user_name,
            "password": password,
            "isSynOpen": is_syn_open,
            "faSecretKey": fa_secret_key,
            "cookie": cookie,
            
            "proxyMethod": proxy_method,
            "proxyType": proxy_type,
            "host": host,
            "port": port, 
            "proxyUserName": proxy_username,
            "proxyPassword": proxy_password,
            "ipCheckService": ip_check_service,
            "isIpv6": is_ipv6,
            "refreshProxyUrl": refresh_proxy_url,
            "country": country,
            "province": province,
            "city": city,
            
            "dynamicIpUrl": dynamic_ip_url,
            "dynamicIpChannel": dynamic_ip_channel,
            "isDynamicIpChangeIp": is_dynamic_ip_change_ip,
            "duplicateCheck": duplicate_check,
            
            "workbench": workbench,
            "abortImage": abort_image,
            "abortImageMaxSize": abort_image_max_size,
            "abortMedia": abort_media,
            "muteAudio": mute_audio,
            "stopWhileNetError": stop_while_net_error,
            "stopWhileIpChange": stop_while_ip_change,
            "stopWhileCountryChange": stop_while_country_change,
            
            "browserFingerPrint": browser_fingerprint
        }
        
        # 清除空值
        data = {k: v for k, v in data.items() if v is not None}
        
        response_data = self._make_request("browser/update", data)
        return BrowserResponse.from_dict(response_data)
    
    def update_browser_partial(self, ids: List[str], **kwargs) -> GenericResponse:
        """
        Update specific properties of one or more browsers.
        
        Args:
            ids: List of browser IDs to update
            **kwargs: Properties to update (name, remark, etc.)
            
        Returns:
            GenericResponse object
        """
        data = {"ids": ids, **kwargs}
        response_data = self._make_request("browser/update/partial", data)
        return GenericResponse.from_dict(response_data)
    
    def browser_list(self, page: int = 0, page_size: int = 10, group_id: Optional[str] = None) -> BrowserListResponse:
        """
        Get a list of browser windows.
        
        Args:
            page: Page number (0-based)
            page_size: Number of items per page
            group_id: Filter by group ID
            
        Returns:
            BrowserListResponse object with list of browsers
        """
        data = {
            "page": page,
            "pageSize": page_size
        }
        if group_id:
            data["groupId"] = group_id
        response_data = self._make_request("browser/list", data)
        return BrowserListResponse.from_dict(response_data)
    
    def browser_list_concise(self, 
                            page: int = 0, 
                            page_size: int = 100, 
                            sort_direction: str = "desc",
                            sort_properties: str = "seq") -> BrowserListResponse:
        """
        Get a concise list of browser windows.
        
        Args:
            page: Page number (0-based)
            page_size: Number of items per page
            sort_direction: Sort direction (asc or desc)
            sort_properties: Property to sort by
            
        Returns:
            BrowserListResponse object with concise list of browsers
        """
        data = {
            "page": page,
            "pageSize": page_size,
            "sortDirection": sort_direction,
            "sortProperties": sort_properties
        }
        response_data = self._make_request("browser/list/concise", data)
        return BrowserListResponse.from_dict(response_data)
    
    def get_browser_pids(self, ids: List[str]) -> BrowserPidResponse:
        """
        Get process IDs for specified browsers.
        
        Args:
            ids: List of browser IDs
            
        Returns:
            BrowserPidResponse object with PIDs
        """
        data = {"ids": ids}
        response_data = self._make_request("browser/pids", data)
        return BrowserPidResponse.from_dict(response_data)
    
    def get_browser_pids_alive(self, ids: List[str]) -> BrowserPidResponse:
        """
        Check if specified browsers are alive and get their PIDs.
        
        Args:
            ids: List of browser IDs
            
        Returns:
            BrowserPidResponse object with alive status and PIDs
        """
        data = {"ids": ids}
        response_data = self._make_request("browser/pids/alive", data)
        return BrowserPidResponse.from_dict(response_data)
    
    def get_all_browser_pids(self) -> BrowserPidResponse:
        """Get PIDs for all browser windows"""
        response_data = self._make_request("browser/pids/all")
        return BrowserPidResponse.from_dict(response_data)
    
    def open_browser(self, 
                       id: str, 
                       args: List[str] = None,
                       queue: bool = False,
                       ignore_default_urls: bool = False,
                       new_page_url: Optional[str] = None) -> BrowserResponse:
        """
        Open a browser window.
        
        Args:
            id: Browser ID
            args: Additional arguments for browser launch
            queue: Whether to open in queue mode (prevents concurrent errors)
            ignore_default_urls: Ignore synced URLs and open only blank page or workbench
            new_page_url: Specify a URL to open during browser launch
            
        Returns:
            BrowserResponse object with browser information including:
            - ws: WebSocket URL for DevTools connection
            - http: HTTP address
            - coreVersion: Chrome core version
            - driver: Path to chromedriver
            - seq: Browser sequence number
            - name: Browser name
            - remark: Browser remark
            - groupId: Group ID
            - pid: Process ID
        """
        data = {"id": id}
        if args:
            data["args"] = args
        if queue:
            data["queue"] = queue
        if ignore_default_urls:
            data["ignoreDefaultUrls"] = ignore_default_urls
        if new_page_url:
            data["newPageUrl"] = new_page_url
            
        response_data = self._make_request("browser/open", data)
        return BrowserResponse.from_dict(response_data)
    
    def close_browser(self, id: str) -> GenericResponse:
        """
        Close a browser window.
        
        Args:
            id: Browser ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("browser/close", data)
        return GenericResponse.from_dict(response_data)
    
    def close_browsers_by_seqs(self, seqs: List[int]) -> GenericResponse:
        """
        Close browser windows by sequence numbers.
        
        Args:
            seqs: List of sequence numbers
            
        Returns:
            GenericResponse object
        """
        data = {"seqs": seqs}
        response_data = self._make_request("browser/close/byseqs", data)
        return GenericResponse.from_dict(response_data)
    
    def delete_browser(self, id: str) -> GenericResponse:
        """
        Delete a browser window.
        
        Args:
            id: Browser ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("browser/delete", data)
        return GenericResponse.from_dict(response_data)
    
    def delete_browsers(self, ids: List[str]) -> GenericResponse:
        """
        Delete multiple browser windows.
        
        Args:
            ids: List of browser IDs
            
        Returns:
            GenericResponse object
        """
        data = {"ids": ids}
        response_data = self._make_request("browser/delete/ids", data)
        return GenericResponse.from_dict(response_data)
    
    def get_browser_detail(self, id: str) -> BrowserResponse:
        """
        Get detailed information about a browser window.
        
        Args:
            id: Browser ID
            
        Returns:
            BrowserResponse object with browser details
        """
        data = {"id": id}
        response_data = self._make_request("browser/detail", data)
        return BrowserResponse.from_dict(response_data)
    
    def reopen_browsers_at_pos(self, ids: List[str], all: bool = False) -> GenericResponse:
        """
        Restart browser windows at their positions.
        
        Args:
            ids: List of browser IDs to restart
            all: Whether to restart all browser windows
            
        Returns:
            GenericResponse object
        """
        data = {"ids": ids, "all": all}
        response_data = self._make_request("browser/reopenAtPos", data)
        return GenericResponse.from_dict(response_data)
    
    def get_browser_ports(self) -> BrowserPidResponse:
        """Get ports for all open browser windows"""
        response_data = self._make_request("browser/ports")
        return BrowserPidResponse.from_dict(response_data)
    
    def update_browser_group(self, group_id: str, browser_ids: List[str]) -> GenericResponse:
        """
        Move browsers to a different group.
        
        Args:
            group_id: Target group ID
            browser_ids: List of browser IDs to move
            
        Returns:
            GenericResponse object
        """
        data = {
            "groupId": group_id,
            "browserIds": browser_ids
        }
        response_data = self._make_request("browser/group/update", data)
        return GenericResponse.from_dict(response_data)
    
    def update_browser_remark(self, remark: str, browser_ids: List[str]) -> GenericResponse:
        """
        Update remarks for browsers.
        
        Args:
            remark: New remark text
            browser_ids: List of browser IDs to update
            
        Returns:
            GenericResponse object
        """
        data = {
            "remark": remark,
            "browserIds": browser_ids
        }
        response_data = self._make_request("browser/remark/update", data)
        return GenericResponse.from_dict(response_data)
    
    def update_browser_proxy(self, 
                            ids: List[str], 
                            proxy_method: int = 2,
                            proxy_type: str = "noproxy",
                            host: str = "",
                            port: str = "",
                            proxy_username: str = "",
                            proxy_password: str = "",
                            **kwargs) -> GenericResponse:
        """
        Update proxy settings for browsers.
        
        Args:
            ids: List of browser IDs
            proxy_method: Proxy method
            proxy_type: Type of proxy
            host: Proxy host
            port: Proxy port
            proxy_username: Proxy authentication username
            proxy_password: Proxy authentication password
            **kwargs: Additional proxy configuration options
            
        Returns:
            GenericResponse object
        """
        data = {
            "ids": ids,
            "proxyMethod": proxy_method,
            "proxyType": proxy_type,
            "host": host,
            "port": port,
            "proxyUserName": proxy_username,
            "proxyPassword": proxy_password,
            **kwargs
        }
        response_data = self._make_request("browser/proxy/update", data)
        return GenericResponse.from_dict(response_data)
    
    # Group management APIs
    def add_group(self, group_name: str, sort_num: int = 0) -> GroupResponse:
        """
        Create a new group.
        
        Args:
            group_name: Name of the group
            sort_num: Sort order
            
        Returns:
            GroupResponse object
        """
        data = {
            "groupName": group_name,
            "sortNum": sort_num
        }
        response_data = self._make_request("group/add", data)
        return GroupResponse.from_dict(response_data)
    
    def edit_group(self, id: str, group_name: str, sort_num: int = 0) -> GroupResponse:
        """
        Edit an existing group.
        
        Args:
            id: Group ID
            group_name: New name for the group
            sort_num: New sort order
            
        Returns:
            GroupResponse object
        """
        data = {
            "id": id,
            "groupName": group_name,
            "sortNum": sort_num
        }
        response_data = self._make_request("group/edit", data)
        return GroupResponse.from_dict(response_data)
    
    def delete_group(self, id: str) -> GenericResponse:
        """
        Delete a group.
        
        Args:
            id: Group ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("group/delete", data)
        return GenericResponse.from_dict(response_data)
    
    def get_group_detail(self, id: str) -> GroupResponse:
        """
        Get detailed information about a group.
        
        Args:
            id: Group ID
            
        Returns:
            GroupResponse object with group details
        """
        data = {"id": id}
        response_data = self._make_request("group/detail", data)
        return GroupResponse.from_dict(response_data)
    
    def get_group_list(self, 
                      page: int = 0, 
                      page_size: int = 10, 
                      all: bool = True,
                      sort_direction: str = "asc",
                      sort_properties: str = "sortNum") -> GroupListResponse:
        """
        Get a list of groups.
        
        Args:
            page: Page number (0-based)
            page_size: Number of items per page
            all: Whether to get all groups
            sort_direction: Sort direction (asc or desc)
            sort_properties: Property to sort by
            
        Returns:
            GroupListResponse object with list of groups
        """
        data = {
            "page": page,
            "pageSize": page_size,
            "all": all,
            "sortDirection": sort_direction,
            "sortProperties": sort_properties
        }
        response_data = self._make_request("group/list", data)
        return GroupListResponse.from_dict(response_data)
    
    # Window management APIs
    def arrange_windows(self, 
                       seq_list: List[int], 
                       type: str = "box",
                       start_x: int = 0,
                       start_y: int = 0,
                       width: int = 800,
                       height: int = 500,
                       col: int = 4,
                       space_x: int = 0,
                       space_y: int = 0,
                       offset_x: int = 50,
                       offset_y: int = 50) -> GenericResponse:
        """
        Arrange browser windows in a specific layout.
        
        Args:
            seq_list: List of browser sequence numbers to arrange
            type: Layout type
            start_x: Starting X position
            start_y: Starting Y position
            width: Window width
            height: Window height
            col: Number of columns
            space_x: Horizontal space between windows
            space_y: Vertical space between windows
            offset_x: X offset
            offset_y: Y offset
            
        Returns:
            GenericResponse object
        """
        data = {
            "type": type,
            "startX": start_x,
            "startY": start_y,
            "width": width,
            "height": height,
            "col": col,
            "spaceX": space_x,
            "spaceY": space_y,
            "offsetX": offset_x,
            "offsetY": offset_y,
            "seqlist": seq_list
        }
        response_data = self._make_request("windowbounds", data)
        return GenericResponse.from_dict(response_data)
    
    def arrange_windows_flexable(self, seq_list: List[int] = None) -> GenericResponse:
        """
        Arrange browser windows in an adaptive layout.
        
        Args:
            seq_list: List of browser sequence numbers to arrange (optional)
            
        Returns:
            GenericResponse object
        """
        data = {"seqlist": seq_list or []}
        response_data = self._make_request("windowbounds/flexable", data)
        return GenericResponse.from_dict(response_data)
    
    # User information API
    def get_user_info(self) -> GenericResponse:
        """Get information about the current user"""
        response_data = self._make_request("userInfo")
        return GenericResponse.from_dict(response_data)
    
    # Proxy checking API
    def check_proxy(self, 
                   host: str,
                   port: int,
                   proxy_type: str,
                   proxy_username: str = "",
                   proxy_password: str = "",
                   id: str = "xxx") -> ProxyCheckResponse:
        """
        Test if a proxy is working properly.
        
        Args:
            host: Proxy host
            port: Proxy port
            proxy_type: Type of proxy (http, socks5, etc.)
            proxy_username: Proxy authentication username
            proxy_password: Proxy authentication password
            id: An ID for the test
            
        Returns:
            ProxyCheckResponse object with proxy test results
        """
        data = {
            "host": host,
            "port": port,
            "proxyType": proxy_type,
            "proxyUserName": proxy_username,
            "proxyPassword": proxy_password,
            "id": id
        }
        response_data = self._make_request("checkagent", data)
        return ProxyCheckResponse.from_dict(response_data)
        
    # 以下是根据文档新增的API方法
    
    def reset_browser_closing_state(self, id: str) -> GenericResponse:
        """
        Reset browser closing state when browser is abnormally closed.
        Only use when browser is already closed but status is still 'closing' or 'opening'.
        
        Args:
            id: Browser ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("browser/closing/reset", data)
        return GenericResponse.from_dict(response_data)
    
    def get_all_displays(self) -> GenericResponse:
        """
        Get information about all displays connected to the system.
        
        Returns:
            GenericResponse object with display information
        """
        response_data = self._make_request("alldisplays")
        return GenericResponse.from_dict(response_data)
    
    def close_all_browsers(self) -> GenericResponse:
        """
        Close all browser windows.
        
        Returns:
            GenericResponse object
        """
        response_data = self._make_request("browser/close/all")
        return GenericResponse.from_dict(response_data)
    
    def clear_browser_cache(self, ids: List[str]) -> GenericResponse:
        """
        Clear cache for specified browsers.
        Will clear all local cache files and server cache files.
        
        Args:
            ids: List of browser IDs
            
        Returns:
            GenericResponse object
        """
        data = {"ids": ids}
        response_data = self._make_request("cache/clear", data)
        return GenericResponse.from_dict(response_data)
    
    def clear_browser_cache_except_extensions(self, ids: List[str]) -> GenericResponse:
        """
        Clear cache for specified browsers but keep extension data.
        
        Args:
            ids: List of browser IDs
            
        Returns:
            GenericResponse object
        """
        data = {"ids": ids}
        response_data = self._make_request("cache/clear/exceptExtensions", data)
        return GenericResponse.from_dict(response_data)
    
    def random_browser_fingerprint(self, browser_id: str) -> GenericResponse:
        """
        Generate random fingerprint for specified browser.
        
        Args:
            browser_id: Browser ID
            
        Returns:
            GenericResponse object with fingerprint data
        """
        data = {"browserId": browser_id}
        response_data = self._make_request("browser/fingerprint/random", data)
        return GenericResponse.from_dict(response_data)
    
    def set_browser_cookies(self, browser_id: str, cookies: List[Dict]) -> GenericResponse:
        """
        Set cookies for an open browser window.
        
        Args:
            browser_id: Browser ID
            cookies: List of cookie objects with name, value, domain, etc.
            
        Returns:
            GenericResponse object
        """
        data = {
            "browserId": browser_id,
            "cookies": cookies
        }
        response_data = self._make_request("browser/cookies/set", data)
        return GenericResponse.from_dict(response_data)
    
    def clear_browser_cookies(self, browser_id: str, save_synced: bool = True) -> GenericResponse:
        """
        Clear cookies for a browser window.
        
        Args:
            browser_id: Browser ID
            save_synced: Whether to keep cookies that have been synced to server
            
        Returns:
            GenericResponse object
        """
        data = {
            "browserId": browser_id,
            "saveSynced": save_synced
        }
        response_data = self._make_request("browser/cookies/clear", data)
        return GenericResponse.from_dict(response_data)
    
    def get_browser_cookies(self, browser_id: str) -> GenericResponse:
        """
        Get cookies from an open browser window.
        
        Args:
            browser_id: Browser ID
            
        Returns:
            GenericResponse object with cookie data
        """
        data = {"browserId": browser_id}
        response_data = self._make_request("browser/cookies/get", data)
        return GenericResponse.from_dict(response_data)
    
    def format_cookies(self, cookie: Any, hostname: str) -> GenericResponse:
        """
        Format cookie data into standard format.
        
        Args:
            cookie: Cookie data (can be string, array, etc.)
            hostname: Domain for the cookie
            
        Returns:
            GenericResponse object with formatted cookie data
        """
        data = {
            "cookie": cookie,
            "hostname": hostname
        }
        response_data = self._make_request("browser/cookies/format", data)
        return GenericResponse.from_dict(response_data)
    
    def run_rpa_task(self, id: str) -> GenericResponse:
        """
        Run an RPA task.
        
        Args:
            id: RPA task ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("rpa/run", data)
        return GenericResponse.from_dict(response_data)
    
    def stop_rpa_task(self, id: str) -> GenericResponse:
        """
        Stop a running RPA task.
        
        Args:
            id: RPA task ID
            
        Returns:
            GenericResponse object
        """
        data = {"id": id}
        response_data = self._make_request("rpa/stop", data)
        return GenericResponse.from_dict(response_data)
    
    def auto_paste(self, browser_id: str, url: str) -> GenericResponse:
        """
        Automatically paste clipboard content into focused input field.
        
        Args:
            browser_id: Browser ID
            url: URL where to paste the content
            
        Returns:
            GenericResponse object
        """
        data = {
            "browserId": browser_id,
            "url": url
        }
        response_data = self._make_request("autopaste", data)
        return GenericResponse.from_dict(response_data)
    
    def read_excel_file(self, filepath: str) -> GenericResponse:
        """
        Read content from an Excel file.
        
        Args:
            filepath: Absolute path to the Excel file
            
        Returns:
            GenericResponse object with file content
        """
        data = {"filepath": filepath}
        response_data = self._make_request("utils/readexcel", data)
        return GenericResponse.from_dict(response_data)
    
    def read_text_file(self, filepath: str) -> GenericResponse:
        """
        Read content from a text file.
        
        Args:
            filepath: Absolute path to the text file
            
        Returns:
            GenericResponse object with file content
        """
        data = {"filepath": filepath}
        response_data = self._make_request("utils/readfile", data)
        return GenericResponse.from_dict(response_data) 