#!/usr/bin/env python3
"""
Basic usage examples for the Bitnet API Python SDK
"""

from bitnet_api import BitnetClient
from requests.exceptions import RequestException
import json


def main():
    # Initialize the client
    client = BitnetClient(host="127.0.0.1", port=54345)

    try:
        # 1. Check API health
        print("Checking API health...")
        health_response = client.health_check()
        print(f"Health check response: {health_response}")
        
        if not health_response.success:
            print("API is not healthy, exiting.")
            return
            
        # 2. Get list of groups
        print("\nGetting group list...")
        groups_response = client.get_group_list()
        print(f"Group list response: {groups_response}")
        
        # Use the first group ID if available
        group_id = None
        if groups_response.success and groups_response.content:
            group_id = groups_response.content[0].id
            print(f"Using group ID: {group_id}")
        
        # 3. Create a new browser window
        print("\nCreating a new browser window...")
        browser_response = client.create_or_update_browser(
            browser_fingerprint={"coreVersion": "104"},
            proxy_type="noproxy"
        )
        print(f"Browser creation response: {browser_response}")
        
        if browser_response.success and browser_response.data:
            browser_id = browser_response.data.id
            print(f"Created browser with ID: {browser_id}")
            
            # 4. Update the browser to move it to a group if we have one
            if group_id:
                print(f"\nMoving browser to group {group_id}...")
                update_response = client.update_browser_group(
                    group_id=group_id,
                    browser_ids=[browser_id]
                )
                print(f"Update response: {update_response}")
            
            # 5. Open the browser window
            print("\nOpening the browser window...")
            open_response = client.open_browser(id=browser_id)
            print(f"Open response: {open_response}")
            
            if open_response.success and open_response.data:
                print(f"Browser opened with WebSocket URL: {open_response.data.ws}")
            
            # 6. Get browser details
            print("\nGetting browser details...")
            detail_response = client.get_browser_detail(id=browser_id)
            print(f"Browser detail response: {detail_response}")
            
            if detail_response.success and detail_response.data:
                browser = detail_response.data
                print(f"Browser name: {browser.name}")
                print(f"Browser sequence: {browser.seq}")
                print(f"Browser group ID: {browser.group_id}")
            
            # 7. Close the browser window after a pause
            input("\nPress Enter to close the browser window...")
            close_response = client.close_browser(id=browser_id)
            print(f"Close response: {close_response}")
            
            # 8. Delete the browser window
            print("\nDeleting the browser window...")
            delete_response = client.delete_browser(id=browser_id)
            print(f"Delete response: {delete_response}")
        
    except RequestException as e:
        print(f"API request failed: {e}")


if __name__ == "__main__":
    main() 