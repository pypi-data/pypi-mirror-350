#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
FlyWing API 基本用法示例

本示例展示了FlyWing API客户端的基本使用方法，包括：
- 用户登录和认证
- 获取代理配置
- 任务管理（检查、创建和接收任务）
- 处理工作时间
"""

import os
import sys
import json
from datetime import datetime, timedelta
from typing import List

# 添加项目根目录到系统路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from flywing_api import FlyWingClient
from flywing_api.models import (
    Task, TaskCheckReq, TaskCreateReq, TaskDetailCreateReq,
    TaskReceiveListReq, TaskReceiveReq, UserRegisterReq, ProxyConfig
)


def auth_demo():
    """演示用户认证流程"""
    print("\n=== 用户认证示例 ===")

    client = FlyWingClient(base_url="http://localhost:8080")

    # 1. 用户登录
    print("1. 用户登录...")
    try:
        # 直接使用login方法，内部已经处理了驼峰命名转换
        login_resp = client.login(username="zhangsan", password="password123")
        print(f"登录成功! 认证令牌: {login_resp.token}")
        print(f"用户信息: ID={login_resp.client_user.id}, 用户名={login_resp.client_user.username}")

        # 演示to_dict方法，转换为API所需的驼峰格式
        dict_data = login_resp.to_dict()
        print(f"转换为服务器字段格式: {dict_data}")

        # 2. 获取用户详细信息
        print("\n2. 获取用户详细信息...")
        user_info = client.get_user_info()
        print(f"用户详情: 用户名={user_info.username}, 管理员={user_info.is_admin}, MAC ID={user_info.mac_id}")

        # 演示User模型的to_dict方法
        user_dict = user_info.to_dict()
        print(f"转换为JSON: {json.dumps(user_dict, ensure_ascii=False, indent=2)}")

    except Exception as e:
        print(f"登录失败: {str(e)}")

        # 3. 尝试注册新用户
        print("\n3. 尝试注册新用户...")
        try:
            # 使用模型创建请求对象
            register_req = UserRegisterReq(
                user_name="new_user",
                password="password123",
                repeat_password="password123",
                mac_id="ABC123DEF456",
                device_info="Windows 10, Chrome 96.0"
            )

            # 转换成API请求格式（小驼峰字段名）
            register_dict = register_req.to_dict()
            print(f"注册请求JSON: {json.dumps(register_dict, ensure_ascii=False, indent=2)}")

            # 发送注册请求
            register_resp = client.register(register_req)
            print(f"注册成功! 认证令牌: {register_resp.token}")
            print(f"新用户信息: ID={register_resp.client_user.id}, 用户名={register_resp.client_user.username}")
        except Exception as e:
            print(f"注册失败: {str(e)}")


def proxy_demo(client: FlyWingClient):
    """演示代理相关操作"""
    print("\n=== 代理配置示例 ===")

    # 1. 获取所有代理配置
    print("1. 获取代理配置列表...")
    proxy_configs = client.get_proxy_config_list()

    if not proxy_configs:
        print("未找到代理配置")
        return None

    print(f"找到 {len(proxy_configs)} 个代理配置:")
    for idx, config in enumerate(proxy_configs):
        print(f"  #{idx + 1}: {config.proxy_name} (ID={config.id}, 类型={config.proxy_type})")

    # 2. 获取特定代理配置
    if proxy_configs:
        config_id = proxy_configs[0].id
        print(f"\n2. 获取ID为 {config_id} 的代理配置详情...")
        proxy_detail = client.get_proxy_config_by_id(config_id)
        print(f"  代理名称: {proxy_detail.proxy_name}")
        print(f"  代理类型: {proxy_detail.proxy_type}")
        print(f"  账户: {proxy_detail.account}")
        print(f"  余额: {proxy_detail.balance}")
        print(f"  有效时间: {proxy_detail.valid_time} 秒")

        # 3. 生成代理
        print(f"\n3. 从配置 {config_id} 生成 2 个代理...")
        try:
            proxies = client.gen_proxy(config_id, 2)
            print(f"  生成了 {len(proxies)} 个代理:")
            for i, proxy in enumerate(proxies):
                print(f"  代理 #{i + 1}: {proxy.host}:{proxy.port} (用户: {proxy.user})")
        except Exception as e:
            print(f"  生成代理失败: {str(e)}")

    return proxy_configs[0] if proxy_configs else None


def task_demo(client: FlyWingClient, proxy_config: ProxyConfig = None):
    """演示任务相关操作"""
    print("\n=== 任务管理示例 ===")

    group_id = "test_group"
    task_name = "test_task"

    # 1. 检查任务是否存在
    print(f"1. 检查任务 '{task_name}' 是否存在...")
    check_req = TaskCheckReq(group_id=group_id, task_name=task_name)

    try:
        task = client.check_task(check_req)
        if task:
            print(f"  任务已存在: ID={task.id}, 名称={task.task_name}")
            task_id = task.id
        else:
            print(f"  任务不存在，将创建新任务...")

            # 2. 创建任务
            if proxy_config:
                print(f"2. 创建新任务 '{task_name}'...")

                # 创建窗口信息JSON
                window_info = {
                    "browserName": "Chrome",
                    "os": "Windows",
                    "resolution": "1920x1080"
                }

                # 创建任务详情
                task_detail = TaskDetailCreateReq(window_info_json=json.dumps(window_info))

                # 创建任务
                create_req = TaskCreateReq(
                    group_id=group_id,
                    group_name="测试组",
                    task_name=task_name,
                    open_url="https://example.com",
                    proxy_config_id=proxy_config.id,
                    proxy_config_name=proxy_config.proxy_name,
                    window_count=1,
                    start_time=datetime.now() + timedelta(minutes=5),
                    task_detail_list=[task_detail]
                )

                try:
                    new_task = client.create_task(create_req)
                    print(f"  任务创建成功: ID={new_task.id}, 名称={new_task.task_name}")
                    task_id = new_task.id
                except Exception as e:
                    print(f"  创建任务失败: {str(e)}")
                    return
            else:
                print("  缺少代理配置，无法创建任务")
                return
    except Exception as e:
        print(f"  检查任务失败: {str(e)}")
        return

    # 3. 获取任务列表
    print("\n3. 获取任务列表...")
    req_list = [TaskReceiveListReq(browser_id="browser1", group_id=group_id)]

    try:
        task_list = client.get_task_list(req_list)
        if task_list:
            print(f"  找到 {len(task_list)} 个任务:")
            for i, task_item in enumerate(task_list):
                print(f"  任务 #{i + 1}: ID={task_item.task_id}, 名称={task_item.task_name}")

            # 4. 接收任务
            if task_list:
                print("\n4. 接收第一个任务...")
                receive_req = TaskReceiveReq(
                    browser_id="browser1",
                    browser_name="Chrome",
                    task_id=task_list[0].task_id,
                    task_name=task_list[0].task_name,
                    group_id=task_list[0].group_id
                )

                try:
                    task_assignment = client.receive_task(receive_req)
                    if task_assignment:
                        print(f"  成功接收任务: 任务ID={task_assignment.task_id}")
                        print(f"  任务详情ID: {task_assignment.task_detail_id}")
                        print(f"  浏览器ID: {task_assignment.browser_id}")
                        print(f"  广告域名: {task_assignment.ad_domain}")

                        if task_assignment.proxy_info:
                            proxy = task_assignment.proxy_info
                            print(f"  代理信息: {proxy.host}:{proxy.port} (用户: {proxy.user})")

                        if task_assignment.domains:
                            print(f"  域名列表: {len(task_assignment.domains)} 个")
                            for i, domain in enumerate(task_assignment.domains[:3]):
                                print(f"    - {domain.domain} ({domain.country_code})")
                            if len(task_assignment.domains) > 3:
                                print(f"    - ... 等 {len(task_assignment.domains) - 3} 个")

                        # 5. 更新任务窗口信息
                        print("\n5. 更新任务窗口信息...")
                        window_info = {
                            "status": "running",
                            "progress": 50,
                            "cookies": ["cookie1", "cookie2"]
                        }

                        try:
                            update_result = client.update_window_info(
                                id=task_assignment.task_detail_id,
                                window_info_json=window_info
                            )
                            print(f"  窗口信息更新结果: {update_result}")

                            # 6. 标记任务完成
                            print("\n6. 标记任务完成...")
                            client.update_complete_info(task_assignment.task_detail_id)
                            print(f"  任务已标记为完成")

                        except Exception as e:
                            print(f"  更新窗口信息失败: {str(e)}")
                    else:
                        print("  未能接收任务")
                except Exception as e:
                    print(f"  接收任务失败: {str(e)}")
        else:
            print("  未找到任务")
    except Exception as e:
        print(f"  获取任务列表失败: {str(e)}")


def working_time_demo(client: FlyWingClient):
    """演示工作时间相关操作"""
    print("\n=== 工作时间示例 ===")

    print("获取所有工作时间配置...")
    try:
        times = client.get_all_working_times()
        print(f"找到 {len(times)} 个工作时间配置:")
        for i, wt in enumerate(times):
            print(f"  #{i + 1}: ID={wt.id}, CST={wt.cst}, PST={wt.pst}, EST={wt.est}, 状态={wt.status}")
    except Exception as e:
        print(f"获取工作时间失败: {str(e)}")


def run_demo():
    """运行完整演示"""
    print("===== FlyWing API 示例程序 =====")

    # 创建API客户端
    client = FlyWingClient(base_url="http://localhost:8080")

    # 运行用户认证演示
    auth_demo()

    # 运行代理演示
    proxy_config = proxy_demo(client)

    # 运行任务演示
    task_demo(client, proxy_config)

    # 运行工作时间演示
    working_time_demo(client)

    print("\n===== 演示完成 =====")


if __name__ == "__main__":
    run_demo()
