import tkinter as tk
import subprocess
import shlex
import threading
import os
import winreg as reg

def set_proxy(enable, server=None, port=None):
    # 打开注册表项
    internet_settings = reg.OpenKey(reg.HKEY_CURRENT_USER,
                                    r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                    0, reg.KEY_ALL_ACCESS)
    
    # 启用或禁用代理
    reg.SetValueEx(internet_settings, 'ProxyEnable', 0, reg.REG_DWORD, 1 if enable else 0)
    
    if enable and server and port:
        # 设置代理服务器地址和端口
        proxy = f"{server}:{port}"
        reg.SetValueEx(internet_settings, 'ProxyServer', 0, reg.REG_SZ, proxy)
    
    # 通知系统代理设置已更改
    import ctypes
    internet_option_refresh = 37
    internet_option_settings_changed = 39
    ctypes.windll.Wininet.InternetSetOptionW(0, internet_option_refresh, 0, 0)
    ctypes.windll.Wininet.InternetSetOptionW(0, internet_option_settings_changed, 0, 0)
    
    # 关闭注册表项
    reg.CloseKey(internet_settings)

class CommandLineTool:
    def __init__(self):
        self.process = None

    def start(self, args):
        if proxy_controlled:
            set_proxy(enable=True, server='127.0.0.1', port=1081) # 启用代理

        startup_info = None
        if self.process is None:
            output_text.insert(tk.END, "打开连接……\n")
            output_text.see(tk.END)
            # 用来隐藏 zju-connect 的控制台窗口
            if os.name == 'nt':
                startup_info = subprocess.STARTUPINFO()
                startup_info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            self.process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True, startupinfo=startup_info)

    def stop(self):
        if proxy_controlled:
            set_proxy(enable=False) # 关闭代理

        if self.process is not None:
            self.process.kill()
            self.process.wait()
            self.process = None
            output_text.insert(tk.END, "关闭连接……\n")
            output_text.see(tk.END)

    def poll(self):
        while self.is_running():
            output = self.process.stdout.readline()
            if output:
                output_text.insert(tk.END, output)
                output_text.see(tk.END)
            root.update_idletasks()

    def is_running(self):
        return self.process is not None and self.process.poll() is None

tool = CommandLineTool()

command = './zju-connect.exe'

def on_connect():
    if tool.is_running():
        status_label.config(text="状态: 正在运行", fg="red")
        return

    username = entry1.get()
    password = entry2.get()
    server_address = var1.get()
    dns_server_address = var2.get()
    
    command_args = [command, "-server", shlex.quote(server_address), "-zju-dns-server", shlex.quote(dns_server_address), "-username", shlex.quote(username), "-password", shlex.quote(password)]
    
    tool.start(command_args)

    status_label.config(text="状态: 正在运行", fg="red")

    t = threading.Thread(target=tool.poll)
    t.daemon = True
    t.start()

def on_disconnect():
    tool.stop()
    status_label.config(text="状态: 已停止", fg="red")

def on_exit():
    tool.stop()
    root.destroy()

def toggle_password_visibility():
    if show_password.get():
        entry2.config(show='')
    else:
        entry2.config(show='*')

def on_entry2_focus_in(event):
    # 在状态栏显示提示信息
    input_method_status_label.config(text="提示: 请切换到英文输入法")

def on_entry2_focus_out(event):
    # 清除状态栏提示信息
    input_method_status_label.config(text="")

root = tk.Tk()
root.title("更适合 HITSZ 宝宝体质的 zju-connect-for-windows")

label1 = tk.Label(root, text="账号：")
label1.pack()
entry1 = tk.Entry(root)
entry1.pack()

label2 = tk.Label(root, text="密码：")
label2.pack()
entry2 = tk.Entry(root, show='*')
entry2.pack()

# 密码框绑定获得焦点和失去焦点事件
entry2.bind("<FocusIn>", on_entry2_focus_in)
entry2.bind("<FocusOut>", on_entry2_focus_out)

show_password = tk.BooleanVar()
show_password.set(False)
toggle_password_visibility()
toggle_password_button = tk.Checkbutton(root, text="显示密码", variable=show_password, command=toggle_password_visibility)
toggle_password_button.pack()

input_method_status_label = tk.Label(root, text="", fg="red")
input_method_status_label.pack(pady=(5, 0))

var1 = tk.StringVar(value="vpn.hitsz.edu.cn")
label3 = tk.Label(root, text="SSL VPN 服务端地址（默认即可）：")
label3.pack()
entry3 = tk.Entry(root, textvariable=var1)
entry3.pack()

var2 = tk.StringVar(value="10.248.98.30")
label4 = tk.Label(root, text="DNS 服务器地址（默认即可）：")
label4.pack()
entry4 = tk.Entry(root, textvariable=var2)
entry4.pack()

# 创建代理启用复选框
proxy_controlled = tk.BooleanVar()
proxy_controlled.set(True)
proxy_checkbox = tk.Checkbutton(root, text="自动配置代理", variable=proxy_controlled)
proxy_checkbox.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=(20, 0))

connect_button = tk.Button(button_frame, text="连接", command=on_connect)
connect_button.pack(side=tk.LEFT, padx=(0, 20))

disconnect_button = tk.Button(button_frame, text="断开", command=on_disconnect)
disconnect_button.pack(side=tk.LEFT, padx=(20, 20))

exit_button = tk.Button(button_frame, text="退出", command=on_exit)
exit_button.pack(side=tk.LEFT, padx=(20, 0))

status_label = tk.Label(root, text="状态: 已停止", fg="red")
status_label.pack(pady=(10, 0))

output_label = tk.Label(root, text="运行信息：")
output_label.pack()
output_text = tk.Text(root)
output_text.pack()

root.mainloop()
