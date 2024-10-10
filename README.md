# HITSZ-connect-for-windows

这个还是太简陋了，推荐使用几乎同时发布但远更完善的 [chenx-dust/HITsz-Connect-for-Windows](https://github.com/chenx-dust/HITsz-Connect-for-Windows)。

## 使用方法

**使用前，请务必先看看下面的“一些说明”。**

步骤：

1. 从本仓库的 [Release](https://github.com/Co-ding-Man/hitsz-connect-for-windows/releases) 页面下载最新版本程序。
2. 确保同目录下有 ``zju-connect.exe``，可从 [zju-connect](https://github.com/Mythologyli/zju-connect) 的 [Release](https://github.com/mythologyli/zju-connect/releases) 页面下载对应平台（Windows）的最新版本。
3. 直接点击运行 ``hitsz-connect-for-windows.exe``，输入账户和密码，点击 ``连接`` 即可。
4. 使用后最好是通过按键“断开”或“退出”，安全关闭程序，否则可能会有未关闭的 ``zju-connect`` 后台程序。

### 写给小白

如果你不是很清楚“代理服务器”是什么，一键运行即可。

### 写给不那么小白的小白

如果你比较清楚“代理服务器”是什么，甚至已经在使用 ``C**sh``、``V*r*y`` 等工具，那你应该知道怎么设置(可以取消勾选“自动配置代理”后自行配置)。当然，如果你不会写分流规则(甚至不知道这是什么)，那么最好的办法可能还是关闭代理软件，然后一键运行本程序。

### 写给非小白

你真的需要这个吗（）

## 一些说明

1. 请确保本程序所在目录下包含可正常运行的可执行程序 ``zju-connect.exe`` (请确保文件名完全一致，~~因为代码里已经写死了~~)。
2. 本程序完全依赖于 [zju-connect](https://github.com/Mythologyli/zju-connect)，是该程序的简陋 Windows GUI 版。
3. 如果遇到问题，可以依次尝试：
   1. 关闭代理软件后重启该程序；
   2. 取消勾选“自动配置代理”，并根据 [Windows 官方教程](https://prod.support.services.microsoft.com/zh-cn/windows/%E5%9C%A8-windows-%E4%B8%AD%E4%BD%BF%E7%94%A8%E4%BB%A3%E7%90%86%E6%9C%8D%E5%8A%A1%E5%99%A8-03096c53-0554-4ffe-b6ab-8b1deee8dae1)，手动设置服务器连接。其中，代理 IP 地址为 ``127.0.0.1``，端口为 ``1081``。然后再点击 ``连接``。

## 从源代码打包

```Bash
pip install nuitka
nuitka --windows-console-mode=disable .\hitsz-connect-for-windows.py
```

## 致谢

+ [EasierConnect](https://github.com/lyc8503/EasierConnect)
+ [zju-connect](https://github.com/Mythologyli/zju-connect)
