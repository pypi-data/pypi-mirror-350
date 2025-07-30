#!/usr/bin/env python3
"""
Example demonstrating group management operations with the Bitnet API Python SDK
"""

from bitnet_api import BitnetClient
from requests.exceptions import RequestException
import time


def main():
    # Initialize the client
    client = BitnetClient(host="127.0.0.1", port=54345)

    try:
        # 1. List existing groups
        print("Listing existing groups...")
        list_response = client.get_group_list()
        print(f"Group list response: {list_response}")
        
        if list_response.success and list_response.content:
            print(f"Found {len(list_response.content)} groups:")
            for i, group in enumerate(list_response.content):
                print(f"  {i+1}. {group.group_name} (ID: {group.id})")
        
        # 2. Create a new group
        print("\nCreating a new group...")
        group_name = f"Test Group {int(time.time())}"  # Add timestamp to make name unique
        group_response = client.add_group(group_name=group_name, sort_num=0)
        print(f"Group creation response: {group_response}")
        
        if group_response.success and group_response.data:
            group_id = group_response.data.id
            print(f"Created group with ID: {group_id}")
            
            # 3. Get group details
            print("\nGetting group details...")
            detail_response = client.get_group_detail(id=group_id)
            print(f"Group detail response: {detail_response}")
            
            if detail_response.success and detail_response.data:
                group = detail_response.data
                print(f"Group details:")
                print(f"  Name: {group.group_name}")
                print(f"  Sort order: {group.sort_num}")
            
            # 4. Create a browser in this group
            print("\nCreating a browser in the new group...")
            browser_response = client.create_or_update_browser(
                browser_fingerprint={"coreVersion": "104"},
                proxy_type="noproxy"
            )
            
            if browser_response.success and browser_response.data:
                browser_id = browser_response.data.id
                print(f"Created browser with ID: {browser_id}")
                
                # 5. Move browser to the new group
                print(f"\nMoving browser to group {group_id}...")
                update_response = client.update_browser_group(
                    group_id=group_id,
                    browser_ids=[browser_id]
                )
                print(f"Update response: {update_response}")
                
                # 6. List browsers in the group
                print(f"\nListing browsers in group {group_id}...")
                browsers_response = client.browser_list(group_id=group_id)
                print(f"Browser list response: {browsers_response}")
                
                if browsers_response.success and browsers_response.content:
                    print(f"Found {len(browsers_response.content)} browsers in group:")
                    for i, browser in enumerate(browsers_response.content):
                        print(f"  {i+1}. {browser.name or 'Unnamed'} (ID: {browser.id})")
                
                # 7. Delete the browser
                print("\nDeleting the browser...")
                delete_response = client.delete_browser(id=browser_id)
                print(f"Delete response: {delete_response}")
            
            # 8. Edit the group
            print("\nEditing the group...")
            edit_response = client.edit_group(
                id=group_id,
                group_name=f"{group_name} - EDITED",
                sort_num=1
            )
            print(f"Edit response: {edit_response}")
            
            if edit_response.success and edit_response.data:
                edited_group = edit_response.data
                print(f"Group edited:")
                print(f"  New name: {edited_group.group_name}")
                print(f"  New sort order: {edited_group.sort_num}")
            
            # 9. Delete the group
            print("\nDeleting the group...")
            delete_response = client.delete_group(id=group_id)
            print(f"Delete response: {delete_response}")
            
            # 10. Verify the group is deleted by listing groups again
            print("\nVerifying deletion by listing groups again...")
            final_list_response = client.get_group_list()
            print(f"Final group list response: {final_list_response}")
            
            # Check if the group is still in the list
            group_still_exists = False
            if final_list_response.success and final_list_response.content:
                for group in final_list_response.content:
                    if group.id == group_id:
                        group_still_exists = True
                        break
            
            if group_still_exists:
                print(f"Group with ID {group_id} still exists!")
            else:
                print(f"Group with ID {group_id} was successfully deleted.")
            
    except RequestException as e:
        print(f"API request failed: {e}")


if __name__ == "__main__":
    main() 