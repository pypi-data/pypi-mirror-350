#!/usr/bin/env python3
"""
Example demonstrating browser management operations with the Bitnet API Python SDK
"""

from bitnet_api import BitnetClient, BrowserFingerPrint
from requests.exceptions import RequestException
import time


def main():
    # Initialize the client
    client = BitnetClient(host="127.0.0.1", port=54345)

    try:
        # 1. List existing browsers
        print("Listing existing browsers...")
        list_response = client.browser_list(page=0, page_size=5)
        print(f"Browser list response: {list_response}")
        
        if list_response.success and list_response.content:
            print(f"Found {len(list_response.content)} browsers:")
            for i, browser in enumerate(list_response.content):
                print(f"  {i+1}. {browser.name or 'Unnamed'} (ID: {browser.id})")
        
        # 2. Create multiple browser windows
        browser_ids = []
        for i in range(3):
            print(f"\nCreating browser window #{i+1}...")
            # Using the BrowserFingerPrint entity
            fingerprint = BrowserFingerPrint(
                core_version="104",
                os="windows",
                os_version="10"
            )
            browser_response = client.create_or_update_browser(
                browser_fingerprint=fingerprint,
                proxy_type="noproxy"
            )
            
            if browser_response.success and browser_response.data:
                browser_id = browser_response.data.id
                browser_ids.append(browser_id)
                print(f"Created browser window #{i+1} with ID: {browser_id}")
        
        # 3. Open all browser windows
        print("\nOpening all browser windows...")
        for i, browser_id in enumerate(browser_ids):
            print(f"Opening browser window #{i+1}...")
            open_response = client.open_browser(id=browser_id)
            if open_response.success:
                print(f"Browser #{i+1} opened successfully.")
                if open_response.data:
                    print(f"  WebSocket URL: {open_response.data.ws}")
                    print(f"  HTTP URL: {open_response.data.http}")
                    print(f"  PID: {open_response.data.pid}")
            else:
                print(f"Failed to open browser #{i+1}. Error: {open_response.msg}")
        
        # 4. Arrange the windows in a grid
        print("\nArranging browser windows in a grid...")
        # First get the sequence numbers
        browser_seqs = []
        for browser_id in browser_ids:
            detail_response = client.get_browser_detail(id=browser_id)
            if detail_response.success and detail_response.data and detail_response.data.seq:
                browser_seqs.append(detail_response.data.seq)
        
        if browser_seqs:
            print(f"Arranging browser sequences: {browser_seqs}")
            arrange_response = client.arrange_windows(
                seq_list=browser_seqs,
                width=800,
                height=600,
                col=2,
                start_x=50,
                start_y=50,
                space_x=20,
                space_y=20
            )
            print(f"Window arrangement response: {arrange_response}")
        
        # 5. Get PIDs for browsers
        print("\nGetting PIDs for browsers...")
        pids_response = client.get_browser_pids(ids=browser_ids)
        print(f"Browser PIDs response: {pids_response}")
        
        if pids_response.success and pids_response.data:
            print("Browser PIDs:")
            for browser_id, pid in pids_response.data.browser_ids.items():
                print(f"  Browser {browser_id}: PID {pid}")
        
        # 6. Update browser remarks
        print("\nUpdating browser remarks...")
        remark_response = client.update_browser_remark(
            remark="Test browser window",
            browser_ids=browser_ids
        )
        print(f"Update remark response: {remark_response}")
        
        # 7. Update one browser's proxy settings
        if browser_ids:
            print("\nUpdating proxy settings for the first browser...")
            proxy_response = client.update_browser_proxy(
                ids=[browser_ids[0]],
                proxy_type="http",
                host="example.com",
                port="8080",
                proxy_username="user",
                proxy_password="pass"
            )
            print(f"Update proxy response: {proxy_response}")
        
        # 8. Wait a moment for user to see the windows
        print("\nBrowser windows are open. Waiting 10 seconds before closing...")
        time.sleep(10)
        
        # 9. Close all browser windows
        print("\nClosing all browser windows...")
        for i, browser_id in enumerate(browser_ids):
            print(f"Closing browser window #{i+1}...")
            close_response = client.close_browser(id=browser_id)
            if close_response.success:
                print(f"Browser #{i+1} closed successfully.")
            else:
                print(f"Failed to close browser #{i+1}. Error: {close_response.msg}")
        
        # 10. Delete all browser windows
        print("\nDeleting all browser windows...")
        delete_response = client.delete_browsers(ids=browser_ids)
        print(f"Delete response: {delete_response}")
        
    except RequestException as e:
        print(f"API request failed: {e}")


if __name__ == "__main__":
    main() 