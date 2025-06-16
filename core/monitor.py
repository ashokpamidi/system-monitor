import ctypes
import psutil
import win32api
import json
import asyncio
import time

from db_operations import save_to_buffer

def make_observation():
    print("making an observation....")
    hwnd = ctypes.windll.user32.GetForegroundWindow()  # Get active window handle
    pid = ctypes.c_ulong()
    ctypes.windll.user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))  # Get process ID
    cursor_position = str(win32api.GetCursorPos())
    
    app_name = None
    cnt = 0
    for process in psutil.process_iter(attrs=['pid', 'name']):
        if process.info['pid'] == pid.value:
            app_name = process.info['name']
        cnt += 1
    
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
    result =  {'timestamp':timestamp, 'total_active_processes': cnt,'app_name': app_name, 'cursor_position': cursor_position}
        
    if app_name is None:
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
        result =  {'timestamp':timestamp, 'total_active_processes': cnt, 'app_name': 'Unknown', 'cursor_position': cursor_position}
    
    return result
