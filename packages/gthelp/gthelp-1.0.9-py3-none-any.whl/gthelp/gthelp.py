#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
__DIR__ = Path(__file__).parent

def check_adb_installed():
    """检查adb是否已安装"""
    try:
        subprocess.run(['adb', 'version'], check=True)
        return True
    except (subprocess.SubprocessError, FileNotFoundError):
        return False

def get_connected_devices():
    """获取已连接的Android设备列表"""
    try:
        result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        devices = []
        for line in result.stdout.decode('utf-8').split('\n')[1:]:
            if line.strip() and 'device' in line:
                devices.append(line.split('\t')[0])
        return devices
    except subprocess.SubprocessError as e:
        print(f"Error getting devices: {e}")
        return []

def exec_helper(device_id=None):
    """
    执行libhelper
    
    Args:        
        device_id (str, optional): 目标设备ID, 如果为None则使用第一个可用设备
    
    Returns:
        bool: 推送是否成功
    """
    helper_path = f"{__DIR__}/assets/arm64-v8a/libhelper"
    if not check_adb_installed():
        print("Error: ADB is not installed or not in PATH")
        return False
    
    if not os.path.exists(helper_path):
        print(f"Error: Tool file not found at {helper_path}")
        return False
    
    devices = get_connected_devices()
    if not devices:
        print("Error: No Android devices connected")
        return False
    
    if device_id is None:
        device_id = devices[0]
    elif device_id not in devices:
        print(f"Error: Device {device_id} not found")
        return False
    
    target_path = "/data/local/tmp/libhelper"
    try:
        # 使用adb push命令推送文件
        cmd = ['adb', '-s', device_id, 'push', helper_path, target_path]
        result = subprocess.run(cmd, check=True)
        print(f"Successfully pushed {helper_path} to {target_path} on device {device_id}")
        
        # Make the library executable
        chmod_cmd = ["adb", '-s', device_id, "shell", "chmod", "+x", "/data/local/tmp/libhelper"]
        subprocess.run(chmod_cmd, check=True)
        
        # Kill the process
        kill_cmd = ["adb", '-s', device_id, "shell", "pkill", "libhelper"]
        subprocess.run(kill_cmd, check=False)
        
        # Execute the library
        exec_cmd = ["adb", '-s', device_id, "shell", "/data/local/tmp/libhelper"]
        subprocess.run(exec_cmd, check=True)        
        return True
    except subprocess.SubprocessError as e:
        print(f"Error pushing file: {e}")
        return False