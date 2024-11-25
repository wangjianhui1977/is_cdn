import socket  # 导入socket模块，用于网络通信
import requests  # 导入requests模块，用于发送HTTP请求

def is_using_cdn(domain):
    """
    判断指定域名是否使用CDN。
    - 通过获取域名的IP地址和HTTP响应头来判断。
    """
    try:
        # 获取域名的所有IP地址
        ip_addresses = socket.getaddrinfo(domain, None)
        unique_ips = set(addr[4][0] for addr in ip_addresses)  # 提取唯一的IP地址
        print(f"IP addresses: {unique_ips}")  # 打印IP地址列表

        # 发送HTTP请求，获取响应头
        response = requests.get(f'http://{domain}', timeout=5)  # 发送HTTP请求，设置超时时间为5秒
        headers = response.headers  # 获取响应头
        print(f"Headers: {headers}")  # 打印响应头

        # 判断条件：
        # - IP地址数量较多
        # - 响应头中包含CDN特征字段
        cdn_headers = ['X-CDN', 'X-Cache', 'CF-Cache-Status', 'Via', 'X-Amz-Cf-Id']  # 定义CDN特征字段
        if len(unique_ips) > 1 or any(header in headers for header in cdn_headers):  # 判断是否使用CDN
            return True  # 返回True表示可能使用CDN
        else:
            return False  # 返回False表示可能没有使用CDN
    except Exception as e:
        print(f"Error: {e}")  # 打印错误信息
        return None  # 返回None表示无法确定

if __name__ == "__main__":
    domain = input("请输入域名：")  # 提示用户输入域名
    result = is_using_cdn(domain)  # 调用函数判断是否使用CDN
    if result is None:
        print(f"无法确定 {domain} 是否使用CDN。")  # 打印无法确定的信息
    elif result:
        print(f"{domain} 可能正在使用CDN。")  # 打印可能使用CDN的信息
    else:
        print(f"{domain} 可能没有使用CDN。")  # 打印可能没有使用CDN的信息