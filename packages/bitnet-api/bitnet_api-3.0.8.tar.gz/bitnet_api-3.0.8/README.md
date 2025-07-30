# Bitnet API Python SDK

A Python SDK for interacting with the Bitnet Browser API.

## Features

- Complete API wrapper for Bitnet Browser API
- Entity-based response models for better type hints and code readability
- Comprehensive documentation and examples
- Modular and extensible design

## Installation

```bash
pip install bitnet-api
```

## Usage

### Initialize the client

```python
from bitnet_api import BitnetClient

# Initialize with default settings (localhost:54345)
client = BitnetClient()

# Or with custom host and port
client = BitnetClient(host="127.0.0.1", port=55055)

# If authentication is required
client = BitnetClient(token="your-auth-token")
```

### Basic operations

#### Health Check

```python
# Check API health
from requests.exceptions import RequestException

try:
    response = client.health_check()
    if response.success:
        print("API is healthy!")
    else:
        print(f"API health check failed: {response.msg}")
except RequestException as e:
    print(f"API request failed: {e}")
```

#### Browser Management

Create or update a browser window:

```python
# Create a new browser window
from bitnet_api import BrowserFingerPrint

# You can use a dictionary for fingerprint configuration
response = client.create_or_update_browser(
    proxy_type="http",
    host="proxy.example.com",
    port="8080",
    proxy_username="user",
    proxy_password="pass",
    browser_fingerprint={"coreVersion": "104"}
)

# Or use the BrowserFingerPrint entity
fingerprint = BrowserFingerPrint(
    core_version="104",
    os="windows",
    os_version="10"
)
response = client.create_or_update_browser(
    proxy_type="socks5",
    host="proxy.example.com",
    port="1080",
    browser_fingerprint=fingerprint
)

if response.success and response.data:
    browser_id = response.data.id
    print(f"Created browser with ID: {browser_id}")
```

Open and close browser windows:

```python
# Open a browser window
response = client.open_browser(id=browser_id)
if response.success and response.data:
    print(f"Browser opened with WebSocket URL: {response.data.ws}")
    print(f"HTTP URL: {response.data.http}")
    print(f"PID: {response.data.pid}")

# Close a browser window
response = client.close_browser(id=browser_id)
if response.success:
    print("Browser closed successfully")
```

List browser windows:

```python
# List all browser windows
response = client.browser_list(page=0, page_size=10)
if response.success and response.content:
    print(f"Found {len(response.content)} browsers:")
    for browser in response.content:
        print(f"Browser: {browser.id} - {browser.name or 'Unnamed'}")

# Get a concise list with specific sorting
response = client.browser_list_concise(sort_properties="name", sort_direction="asc")
```

Delete browser windows:

```python
# Delete a single browser window
response = client.delete_browser(id=browser_id)
if response.success:
    print("Browser deleted successfully")

# Delete multiple browser windows
response = client.delete_browsers(ids=["id1", "id2", "id3"])
if response.success:
    print("Multiple browsers deleted successfully")
```

#### Group Management

```python
# Create a new group
response = client.add_group(group_name="My Test Group")
if response.success and response.data:
    group_id = response.data.id
    print(f"Created group with ID: {group_id}")

# List all groups
response = client.get_group_list()
if response.success and response.content:
    print(f"Found {len(response.content)} groups:")
    for group in response.content:
        print(f"Group: {group.id} - {group.group_name}")

# Move browsers to a group
response = client.update_browser_group(group_id=group_id, browser_ids=[browser_id])
if response.success:
    print("Browsers moved to group successfully")

# Delete a group
response = client.delete_group(id=group_id)
if response.success:
    print("Group deleted successfully")
```

#### Window Arrangement

```python
# Arrange windows in a grid
response = client.arrange_windows(
    seq_list=[1, 2, 3, 4],
    width=800,
    height=600,
    col=2
)
if response.success:
    print("Windows arranged successfully")

# Auto-arrange all windows
response = client.arrange_windows_flexable()
if response.success:
    print("Windows auto-arranged successfully")
```

#### Proxy Testing

```python
# Test if a proxy is working
response = client.check_proxy(
    host="proxy.example.com",
    port=8080,
    proxy_type="http",
    proxy_username="user",
    proxy_password="pass"
)
if response.success and response.data:
    proxy_info = response.data
    print(f"Proxy is working! IP: {proxy_info.ip}")
    print(f"Location: {proxy_info.city}, {proxy_info.state_prov}, {proxy_info.country_name}")
else:
    print("Proxy test failed")
```

## Examples

Check the [examples directory](examples/) for more usage examples:

- [Basic Usage](examples/basic_usage.py)
- [Browser Management](examples/browser_management.py)
- [Group Management](examples/group_management.py)
- [Proxy Testing](examples/proxy_testing.py)

## Running Tests

To run the tests, clone the repository and install the package in development mode:

```bash
git clone https://github.com/dekinsq/bit_api.git
cd bit_api
pip install -e .
```

Then run the tests:

```bash
# Run basic entity tests
python tests/basic_test.py

# Run client tests with mock server
python tests/client_test.py
```

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Response Format

All API methods return entity objects containing structured data, not raw dictionaries. This provides better type hints and makes the API more user-friendly.

Available entities include:

- `BaseResponse` - Base class for all responses with success and error information
- `Browser` - Browser window details
- `Group` - Group details
- `BrowserFingerPrint` - Browser fingerprint configuration
- `BrowserListResponse` - Response containing list of browsers
- `GroupListResponse` - Response containing list of groups
- `ProxyCheckInfo` - Information about proxy check results
- and more...

## Error Handling

The SDK uses `requests.raise_for_status()` to raise exceptions for HTTP errors. You should wrap your API calls in try-except blocks:

```python
from requests.exceptions import RequestException

try:
    response = client.health_check()
    # Process response
except RequestException as e:
    print(f"API request failed: {e}")
```

## Package Publishing

This project includes several tools to simplify version management and publishing to PyPI.

### Publishing Tools Overview

| Tool | Type | Functionality |
|-----|------|------|
| `publish.sh` | Shell script | Basic publishing automation |
| `publish.py` | Python script | Full-featured publishing tool with argument parsing and test publishing support |
| `bump_version.py` | Python script | Standalone version updater |

### Using `publish.py` (Recommended)

This is the most complete publishing tool with version management and publishing functionality.

```bash
# Increment patch version and publish
python publish.py patch

# Increment minor version and publish
python publish.py minor

# Increment major version and publish
python publish.py major

# Publish to TestPyPI
python publish.py patch --test

# Skip confirmation prompts
python publish.py patch --no-confirm
```

**Parameters:**

- `patch|minor|major`: Specify which version part to increment
- `--no-confirm`: Skip confirmation steps
- `--test`: Upload to TestPyPI instead of the official PyPI

### Using `publish.sh`

A simple shell script that provides basic publishing functionality.

```bash
./publish.sh
```

### Using `bump_version.py`

If you only want to update the version number without publishing:

```bash
# Increment patch version
python bump_version.py patch

# Increment minor version
python bump_version.py minor

# Increment major version
python bump_version.py major
```

### PyPI Configuration

The publishing tools require a `~/.pypirc` file for authentication:

```
[pypi]
username = __token__
password = your-pypi-token

[testpypi]
username = __token__
password = your-testpypi-token
```

See [README_PUBLISH.md](README_PUBLISH.md) for more detailed publishing instructions.

## Complete API Reference

For a complete list of available methods and entity models, check the class documentation or refer to the official Bitnet API documentation. 

## AdsPower API 客户端

这是一个用于与AdsPower浏览器指纹管理工具进行交互的Python客户端库。通过这个库，你可以创建、启动、停止、更新和删除浏览器环境，以及查询环境和分组信息。

### 安装

```bash
# 从项目目录安装
cd /path/to/bit_api
pip install -e .
```

### 快速开始

#### 初始化客户端

```python
from adspower_api import AdsPowerClient

# 默认连接到本地AdsPower服务
client = AdsPowerClient(host="127.0.0.1", port=50325)
```

#### 创建浏览器环境

```python
from adspower_api import AdsPowerClient, BrowserFingerprint, UserProxyConfig

# 初始化客户端
client = AdsPowerClient()

# 创建指纹配置
fingerprint = BrowserFingerprint(
    automatic_timezone="1",
    webrtc="proxy",
    language=["zh-CN", "en-US"],
    resolution="1920,1080",
    platform="win32"
)

# 创建代理配置
proxy_config = UserProxyConfig(
    proxy_soft="other",
    proxy_type="http",
    proxy_host="127.0.0.1",
    proxy_port="8080",
    proxy_user="username",
    proxy_password="password"
)

# 创建浏览器环境
response = client.create_browser(
    group_id="12345",  # 替换为实际的分组ID
    name="测试浏览器",
    remark="API创建的测试环境",
    fingerprint_config=fingerprint,
    user_proxy_config=proxy_config
)

if response.code == 0:
    print(f"创建成功，环境ID: {response.data.profile_id}")
else:
    print(f"创建失败: {response.msg}")
```

#### 启动浏览器

```python
response = client.start_browser(
    profile_id="your_profile_id",
    headless="0",  # 非无头模式
    proxy_detection="0"  # 不打开代理检测页面
)

if response.code == 0:
    print(f"启动成功，调试地址: {response.data.ws}")
    print(f"浏览器地址: {response.data.webdriver}")
else:
    print(f"启动失败: {response.msg}")
```

#### 查询浏览器环境列表

```python
response = client.list_browsers(page=1, limit=10)

if response.code == 0:
    print(f"总数: {response.data.page_info.total}")
    for browser in response.data.list:
        print(f"ID: {browser.profile_id}, 名称: {browser.name}, 状态: {browser.status}")
else:
    print(f"查询失败: {response.msg}")
```

#### 查询分组列表

```python
response = client.list_groups(page=1, page_size=10)

if response.code == 0:
    print(f"总数: {response.data.page_info.total}")
    for group in response.data.list:
        print(f"ID: {group.group_id}, 名称: {group.group_name}")
else:
    print(f"查询失败: {response.msg}")
```

#### 关闭浏览器

```python
response = client.stop_browser(profile_id="your_profile_id")

if response.code == 0:
    print("关闭成功")
else:
    print(f"关闭失败: {response.msg}")
```

#### 更新浏览器环境

```python
response = client.update_browser(
    profile_id="your_profile_id",
    name="更新后的名称",
    remark="API更新的环境"
)

if response.code == 0:
    print("更新成功")
else:
    print(f"更新失败: {response.msg}")
```

#### 删除浏览器环境

```python
response = client.delete_browser(profile_id=["your_profile_id"])

if response.code == 0:
    print("删除成功")
else:
    print(f"删除失败: {response.msg}")
```