#!/usr/bin/env python3
"""
Example demonstrating proxy testing operations with the Bitnet API Python SDK
"""

from bitnet_api import BitnetClient
from requests.exceptions import RequestException


def main():
    # Initialize the client
    client = BitnetClient(host="127.0.0.1", port=54345)

    try:
        # 1. Test HTTP proxy
        print("Testing HTTP proxy...")
        http_proxy_response = client.check_proxy(
            host="example-proxy.com",
            port=8080,
            proxy_type="http",
            proxy_username="user1",
            proxy_password="pass1"
        )
        print(f"HTTP proxy test response: {http_proxy_response}")
        
        if http_proxy_response.success and http_proxy_response.data:
            proxy_info = http_proxy_response.data
            print(f"HTTP proxy is working!")
            print(f"  IP: {proxy_info.ip}")
            print(f"  Location: {proxy_info.city}, {proxy_info.state_prov}, {proxy_info.country_name}")
        
        # 2. Test SOCKS5 proxy
        print("\nTesting SOCKS5 proxy...")
        socks5_proxy_response = client.check_proxy(
            host="example-socks.com",
            port=1080,
            proxy_type="socks5",
            proxy_username="user2",
            proxy_password="pass2"
        )
        print(f"SOCKS5 proxy test response: {socks5_proxy_response}")
        
        if socks5_proxy_response.success and socks5_proxy_response.data:
            proxy_info = socks5_proxy_response.data
            print(f"SOCKS5 proxy is working!")
            print(f"  IP: {proxy_info.ip}")
            print(f"  Location: {proxy_info.city}, {proxy_info.state_prov}, {proxy_info.country_name}")
        
        # 3. Test local SOCKS5 proxy without authentication
        print("\nTesting local SOCKS5 proxy without authentication...")
        local_proxy_response = client.check_proxy(
            host="127.0.0.1",
            port=1080,
            proxy_type="socks5"
        )
        print(f"Local SOCKS5 proxy test response: {local_proxy_response}")
        
        if local_proxy_response.success and local_proxy_response.data:
            proxy_info = local_proxy_response.data
            print(f"Local SOCKS5 proxy is working!")
            print(f"  IP: {proxy_info.ip}")
            print(f"  Location: {proxy_info.city}, {proxy_info.state_prov}, {proxy_info.country_name}")
        
        # 4. Create a browser with HTTP proxy
        print("\nCreating a browser with HTTP proxy...")
        browser_response = client.create_or_update_browser(
            proxy_method=2,
            proxy_type="http",
            host="example-proxy.com",
            port="8080",
            proxy_username="user1",
            proxy_password="pass1",
            browser_fingerprint={"coreVersion": "104"}
        )
        print(f"Browser creation response: {browser_response}")
        
        if browser_response.success and browser_response.data:
            browser_id = browser_response.data.id
            print(f"Created browser with ID: {browser_id}")
            print(f"  Proxy type: {browser_response.data.proxy_type}")
            print(f"  Proxy host: {browser_response.data.host}:{browser_response.data.port}")
            
            # 5. Update proxy settings
            print("\nUpdating browser proxy settings...")
            update_response = client.update_browser_proxy(
                ids=[browser_id],
                proxy_type="socks5",
                host="example-socks.com",
                port="1080",
                proxy_username="user2",
                proxy_password="pass2"
            )
            print(f"Proxy update response: {update_response}")
            
            # 6. Get browser details to verify proxy update
            print("\nGetting browser details to verify proxy settings...")
            detail_response = client.get_browser_detail(id=browser_id)
            print(f"Browser detail response: {detail_response}")
            
            if detail_response.success and detail_response.data:
                browser = detail_response.data
                print(f"Updated browser details:")
                print(f"  Proxy type: {browser.proxy_type}")
                print(f"  Proxy host: {browser.host}:{browser.port}")
                print(f"  Proxy auth: {browser.proxy_user_name}:{'*' * len(browser.proxy_password or '')}")
            
            # 7. Delete the browser
            print("\nDeleting the browser...")
            delete_response = client.delete_browser(id=browser_id)
            print(f"Delete response: {delete_response}")
            
    except RequestException as e:
        print(f"API request failed: {e}")


if __name__ == "__main__":
    main() 