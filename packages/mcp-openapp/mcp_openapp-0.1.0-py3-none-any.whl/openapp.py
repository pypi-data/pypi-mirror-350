import os
import subprocess
import winreg

from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("openapp")
mcp = FastMCP("openapp", port=9000)

apps = []


@mcp.tool()
async def scan_installed_apps():
    """
    扫描已安装应用列表
    :return: 应用名称和路径列表
    """
    # 读取系统注册表
    reg_paths = [
        r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Classes\Local Settings\Software\Microsoft\Windows\CurrentVersion\AppModel\Repository\Packages",
        r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall",
        r"SOFTWARE\Wow6432Node\Clients\StartMenuInternet",
    ]
    apps = []
    for reg_path in reg_paths:
        for root_key in [winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER]:
            try:
                key = winreg.OpenKey(root_key, reg_path)
                count = winreg.QueryInfoKey(key)[0]
                for i in range(count):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        subkey = winreg.OpenKey(key, subkey_name)

                        name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        path_tuple = winreg.QueryValueEx(subkey, "InstallLocation")
                        path = path_tuple[0].replace('"', '') if path_tuple else ""
                        exe_tuple = winreg.QueryValueEx(subkey, "DisplayIcon")
                        exe = exe_tuple[0].replace('"', '') if exe_tuple else ""
                        if "," in exe:
                            exe = exe.split(",")[0]

                        apps.append({
                            "name": name.lower(),
                            "path": exe if exe.endswith('.exe') else os.path.join(path, exe)
                        })
                    except WindowsError as e:
                        # 可以记录更详细的调试信息
                        # print(f"读取子键失败: {subkey_name}, 错误: {e}")
                        continue
            except WindowsError as e:
                # 某些注册表路径可能不存在，如 WOW6432Node 在 32 位系统上
                print(f"无法打开注册表路径: {root_key}\\{reg_path}，错误: {e}")
                continue

    return apps


@mcp.tool()
async def find_app(apps, keyword):
    """
    在应用列表中根据关键词查找对应应用
    :param apps: 应用列表，如果为空重新获取
    :param keyword: 关键词
    :return: 应用名称列表
    """
    if not apps:
        apps = await scan_installed_apps()
    return [app for app in apps if keyword in app["name"]]


@mcp.tool()
async def launch(name):
    """
    运行app
    :param name: 应用名称
    :return: 执行信息
    """
    matches = await find_app(apps, name)
    if len(matches) == 0:
        return "未找到应用"
    else:
        try:
            print(f"匹配到的应用路径: {matches[0]['path']}")
            subprocess.Popen(matches[0]["path"], shell=True)
            return "已启动"
        except Exception as e:
            return f"启动失败: {str(e)}"


async def main():
    #  测试
    result = await launch("腾讯会议")
    print(result)


if __name__ == "__main__":
    # mcp.run(transport="stdio")
    mcp.run(transport="sse")
    # asyncio.run(main())
