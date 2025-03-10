import sys  # 必须添加这行: 导入 sys 模块 - 非常重要的修复!
print("DEBUG_START: Python 脚本开始运行", file=sys.stderr)  # 调试开始标记 (输出到错误流) - 务必是第一行

import pyaes
import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime


print("----- generate_subscription.py 脚本开始执行 -----", file=sys.stderr)  # 添加脚本启动日志 (输出到错误流)

a = 'http://api.skrapp.net/api/serverlist'
b = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
c = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
d = b'65151f8d966bf596'
e = b'88ca0f0ea1ecf975'

print("----- 定义解密函数 -----", file=sys.stderr)  # 添加日志 (输出到错误流)
def f(g, d, e):
    h = pyaes.AESModeOfOperationCBC(d, iv=e)
    i = b''.join(h.decrypt(g[j:j+16]) for j in range(0, len(g), 16))
    return i[:-i[-1]]

print("----- 发送 POST 请求到 API -----", file=sys.stderr)  # 添加日志 (输出到错误流)
try:
    j = requests.post(a, headers=b, data=c, timeout=10)  # 添加请求超时时间 (10秒), 并捕获异常
    print(f"----- API 请求状态码: {j.status_code} -----", file=sys.stderr)  # 打印请求状态码 (输出到错误流)
    j.raise_for_status()  # 检查 HTTP 状态码，非 200 状态码会抛出异常
except requests.exceptions.RequestException as err:  # 捕获 requests 库的异常
    print(f"----- API 请求失败! 错误信息: {err} -----", file=sys.stderr)  # 打印详细错误信息 (输出到错误流)
    print("----- generate_subscription.py 脚本执行出错并结束 -----", file=sys.stderr)  # 脚本结束日志 (错误) (输出到错误流)
    sys.exit(1)  #  程序出错时，使用 sys.exit(1) 退出

k = j.text.strip()
print(f"----- API 响应文本 (原始数据, 前 100 字符): {k[:100]}... -----", file=sys.stderr)  # 打印 API 响应文本 (前 100 字符) (输出到错误流)

try:
    l = binascii.unhexlify(k)
    print("----- API 响应数据 Hex 解码成功 -----", file=sys.stderr)  # 添加日志 (输出到错误流)
except binascii.Error as err:  # 捕获 binascii 解码异常
    print(f"----- binascii.unhexlify() 解码失败! 错误信息: {err} -----", file=sys.stderr)  # 打印详细错误信息 (输出到错误流)
    print("----- generate_subscription.py 脚本执行出错并结束 -----", file=sys.stderr)  # 脚本结束日志 (错误) (输出到错误流)
    sys.exit(1)

try:
    m = f(l, d, e)
    print("----- AES 解密成功 -----", file=sys.stderr)  # 添加日志 (输出到错误流)
except Exception as err:  # 捕获 AES 解密异常
    print(f"----- AES 解密失败! 错误信息: {err} -----", file=sys.stderr)  # 打印详细错误信息 (输出到错误流)
    print("----- generate_subscription.py 脚本执行出错并结束 -----", file=sys.stderr)  # 脚本结束日志 (错误) (输出到错误流)
    sys.exit(1)


try:
    n = json.loads(m)
    print("----- JSON 解析成功 -----", file=sys.stderr)  # 添加日志 (输出到错误流)
    print("\n----- JSON 数据 (n['data'] 部分 - 前 3 个节点信息) -----")  #  添加分隔符，方便查看 (只打印前 3 个元素，避免日志过长)
    for i, item in enumerate(n['data']):  # 遍历 n['data'] 并打印前 3 个元素
        if i >= 3:
            break  #  只打印前 3 个元素
        print(f"节点 {i+1}: {item}")
    print("----- JSON 数据 (n['data'] 部分 - 前 3 个节点信息) 打印结束 -----\n")
except json.JSONDecodeError as err:  # 捕获 JSON 解析异常
    print(f"----- JSON 解析失败! 错误信息: {err} -----", file=sys.stderr)  # 打印详细错误信息 (输出到错误流)
    print("----- 解密后的内容 (原始数据, 前 500 字符): -----", file=sys.stderr)  # 打印解密后的内容 (前 500 字符) (输出到错误流)
    print(f"{m[:500].decode('utf-8', errors='ignore')}...")  #  打印解密后的内容 (前 500 字符), 忽略解码错误
    print("----- generate_subscription.py 脚本执行出错并结束 -----", file=sys.stderr)  # 脚本结束日志 (错误) (输出到错误流)
    sys.exit(1)


ss_urls = []
for o in n['data']:
    p = f"aes-256-cfb:{o['password']}@{o['ip']}:{o['port']}"
    q = base64.b64encode(p.encode('utf-8')).decode('utf-8')
    r = f"ss://{q}#{o['title']}"
    ss_urls.append(r)

subscription_link_content = "\n".join(ss_urls)
subscription_link_base64 = base64.b64encode(subscription_link_content.encode('utf-8')).decode('utf-8')
subscription_link = f"ss://{subscription_link_base64}"

print("----- 订阅链接生成成功 -----", file=sys.stderr)  # 添加日志 (输出到错误流)
print("----- generate_subscription.py 脚本执行成功并结束 -----", file=sys.stderr)  # 脚本结束日志 (成功) (输出到错误流)

print(subscription_link)  #  只打印订阅链接到标准输出
