# AdsPower API 客户端使用示例
import json
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# 现在可以导入adspower_api模块
from adspower_api import AdsPowerClient, BrowserFingerprint, UserProxyConfig

def create_browser_example():
    """创建浏览器环境示例"""
    # 初始化客户端
    client = AdsPowerClient(host="127.0.0.1", port=50325)
    
    # 创建指纹配置
    fingerprint = BrowserFingerprint(
        # 浏览器分辨率
        # screen_resolution="1920_1080",
        screen_resolution="random",
        # 浏览器语言
        language=["en-US", "en"],
        # WebRTC
        webrtc="disabled",
        # 时区
        timezone="America/New_York",
        # 地理位置
        location="allow",
        # 字体
        fonts=["Arial", "Times New Roman"],
        # Canvas
        canvas="1",
        # WebGL图像
        webgl_image="1",
        # WebGL
        webgl="3",
        # 音频
        audio="1",
        # Do Not Track
        do_not_track="true",
        browser_kernel_config={
            "version": "ua_auto",
            "type":"chrome"
        },
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
        group_id="6345582",  # 替换为实际的分组ID
        name="测试浏览器-DQ",
        remark="API创建的测试环境-DQ",
        fingerprint_config=fingerprint,
        user_proxy_config=proxy_config
    )

    print(f'创建浏览器环境: {response}')
    
    if response.code == 0:
        print(f"创建成功，环境ID: {response.browser.profile_id}")
    else:
        print(f"创建失败: {response.msg}")
    
    return response


def start_browser_example(profile_id):
    """启动浏览器示例"""
    client = AdsPowerClient()
    response = client.start_browser(
        profile_id=profile_id,
        headless="0",  # 非无头模式
        proxy_detection="0"  # 不打开代理检测页面
    )
    
    if response.code == 0:
        print(f"启动成功，调试地址: {response}")
    else:
        print(f"启动失败: {response.msg}")
    
    return response


def list_browsers_example():
    """查询浏览器环境列表示例"""
    client = AdsPowerClient()
    response = client.list_browsers(page=1, limit=10)
    
    if response.code == 0:
        print(f"总数: {response.data.page_info.total}")
        for browser in response.data.list:
            print(f"ID: {browser.profile_id}, 名称: {browser.name}, 状态: {browser.status}")
    else:
        print(f"查询失败: {response.msg}")
    
    return response


def list_groups_example():
    """查询分组列表示例"""
    client = AdsPowerClient()
    response = client.list_groups(page=1, page_size=10)
    
    print(f'查询分组信息: {response}')

    if response.code == 0:
        # print(f"总数: {response.data.page_info.total}") # PageInfo does not have 'total' attribute
        for group in response.groups:
            print(f"ID: {group.group_id}, 名称: {group.group_name}, 备注: {group.remark}")
        
    else:
        print(f"查询失败: {response.msg}")
    
    return response


def check_browser_active_example(profile_id):
    """检查浏览器活动状态示例"""
    client = AdsPowerClient()
    response = client.check_browser_active(profile_id=profile_id)

    print(f'查询浏览器状态: {response}')
    
    if response.code == 0:
        if response.status == "Active":
            print(f"浏览器活动中，调试地址: {response.puppeteer}")
            print(f"浏览器地址: {response.webdriver}")
        else:
            print("浏览器未启动")
    else:
        print(f"查询失败: {response.msg}")
    
    return response


def stop_browser_example(profile_id):
    """关闭浏览器示例"""
    client = AdsPowerClient()
    response = client.stop_browser(profile_id=profile_id)
    
    if response.code == 0:
        print("关闭成功")
    else:
        print(f"关闭失败: {response.msg}")
    
    return response


def update_browser_example(profile_id):
    """更新浏览器环境示例"""
    client = AdsPowerClient()
    response = client.update_browser(
        profile_id=profile_id,
        name="更新后的名称",
        remark="API更新的环境"
    )
    
    if response.code == 0:
        print("更新成功")
    else:
        print(f"更新失败: {response.msg}")
    
    return response


def delete_browser_example(profile_id):
    """删除浏览器环境示例"""
    client = AdsPowerClient()
    response = client.delete_browser(profile_id=[profile_id])
    
    if response.code == 0:
        print("删除成功")
    else:
        print(f"删除失败: {response.msg}")
    
    return response


def main():
    """运行完整流程示例"""
    # 检查API接口状态
    status_response = check_status_example()
    if status_response.code != 0:
        print("API接口不可用，无法继续执行")
        return
    
    # 查询分组
    groups_response = list_groups_example()
    if groups_response.code != 0 or not groups_response.groups:
        print("无法获取分组信息或没有可用分组")
        return
    
    # 使用第一个分组创建浏览器
    group_id = groups_response.groups[0].group_id
    print(f"使用分组ID: {group_id}")
    
    # 创建浏览器环境
    create_response = create_browser_example()
    if create_response.code != 0:
        print("创建浏览器环境失败")
        return
    
    profile_id = create_response.browser.profile_id
    print(f"创建的环境ID: {profile_id}")
    
    # 启动浏览器
    start_response = start_browser_example(profile_id)
    if start_response.code != 0:
        print("启动浏览器失败")
        return
    
    # 检查浏览器状态
    active_response = check_browser_active_example(profile_id)
    if active_response.code != 0 or not active_response.status:
        print("浏览器未成功启动")
        return
    
    print("浏览器已成功启动，等待10秒后关闭...")
    import time
    time.sleep(10)
    
    # 关闭浏览器
    stop_response = stop_browser_example(profile_id)
    if stop_response.code != 0:
        print("关闭浏览器失败")
        return
    
    # 更新浏览器信息
    update_response = update_browser_example(profile_id)
    if update_response.code != 0:
        print("更新浏览器信息失败")
        return
    
    # 删除浏览器
    delete_response = delete_browser_example(profile_id)
    if delete_response.code != 0:
        print("删除浏览器失败")
        return
    
    print("完整流程执行成功")


def check_status_example():
    """检查API接口状态示例"""
    # 初始化客户端
    client = AdsPowerClient(host="127.0.0.1", port=50325)
    
    # 检查API接口状态
    response = client.check_status()
    
    if response.code == 0:
        print("API接口可用")
    else:
        print(f"API接口不可用: {response.msg}")
    
    return response

if __name__ == "__main__":
    
    # 或者运行完整流程
    # main()
    
    # 默认只打印可用示例函数
    # print("可用示例函数:")
    # print("- create_browser_example()")
    # print("- start_browser_example(profile_id)")
    # print("- list_browsers_example()")
    # print("- list_groups_example()")
    # print("- check_browser_active_example(profile_id)")
    # print("- stop_browser_example(profile_id)")
    # print("- update_browser_example(profile_id)")
    # print("- delete_browser_example(profile_id)")
    # print("- check_status_example()")
    # print("- main() # 运行完整流程")

    client = AdsPowerClient()
    response = client.start_browser(
        profile_id='kyhnllj',
        headless="0",  # 非无头模式
        proxy_detection="0"  # 不打开代理检测页面
    )
    print(response)

