import sys
import requests
import base64
import json
import pyaes
import binascii
import yaml
import socket
from datetime import datetime

# 定义全局变量
API_URL = 'http://api.skrapp.net/api/serverlist'
HEADERS = {
    'accept': '/',
    'accept-language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
    'appversion': '1.3.1',
    'user-agent': 'SkrKK/1.3.1 (iPhone; iOS 13.5; Scale/2.00)',
    'content-type': 'application/x-www-form-urlencoded',
    'Cookie': 'PHPSESSID=fnffo1ivhvt0ouo6ebqn86a0d4'
}
POST_DATA = {'data': '4265a9c353cd8624fd2bc7b5d75d2f18b1b5e66ccd37e2dfa628bcb8f73db2f14ba98bc6a1d8d0d1c7ff1ef0823b11264d0addaba2bd6a30bdefe06f4ba994ed'}
KEY = b'65151f8d966bf596'
IV = b'88ca0f0ea1ecf975'

def aes_decrypt(ciphertext, key, iv):
    """AES 解密函数"""
    aes = pyaes.AESModeOfOperationCBC(key, iv=iv)
    decrypted = b''.join(aes.decrypt(ciphertext[i:i+16]) for i in range(0, len(ciphertext), 16))
    return decrypted[:-decrypted[-1]]

def check_node(ip, port):
    """检查节点连通性"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((ip, port))
            return True
    except Exception as e:
        return False

def generate_clash_config(nodes):
    """生成 Clash 配置"""
    return {
        'proxies': [
            {
                'name': node['title'],
                'type': 'ss',
                'server': node['ip'],
                'port': node['port'],
                'cipher': node.get('method', 'aes-256-gcm'),  # 动态获取加密方式
                'password': node['password'],
                'udp': True
            } for node in nodes['data']
        ],
        'proxy-groups': [
            {
                'name': '🚀 自动选优',
                'type': 'url-test',
                'url': 'http://cp.cloudflare.com/generate_204',  # 使用 Cloudflare 测速地址
                'interval': 300,  # 每 5 分钟测速一次
                'proxies': [node['title'] for node in nodes['data']]
            },
            {
                'name': '🌍 手动选择',
                'type': 'select',
                'proxies': ['🚀 自动选优'] + [node['title'] for node in nodes['data']]
            }
        ],
        'rules': [
            'MATCH,🚀 自动选优'
        ]
    }

def main():
    print("----- 脚本开始运行 -----", file=sys.stderr)
    
    try:
        # 1. 发送 POST 请求获取加密数据
        print("正在请求节点数据...", file=sys.stderr)
        response = requests.post(API_URL, headers=HEADERS, data=POST_DATA, timeout=10)
        response.raise_for_status()
        print(f"请求状态码: {response.status_code}", file=sys.stderr)

        # 2. 解密数据
        print("正在解密数据...", file=sys.stderr)
        encrypted_data = binascii.unhexlify(response.text.strip())
        decrypted_data = aes_decrypt(encrypted_data, KEY, IV)
        nodes = json.loads(decrypted_data)
        
        # 3. 打印节点信息（前 3 个）
        print("\n----- 节点信息（前 3 个）-----", file=sys.stderr)
        for i, node in enumerate(nodes['data'][:3]):
            print(f"节点 {i+1}: {node}", file=sys.stderr)
        
        # 4. 过滤不可用节点
        print("\n正在检查节点连通性...", file=sys.stderr)
        valid_nodes = []
        for node in nodes['data']:
            if check_node(node['ip'], node['port']):
                valid_nodes.append(node)
                print(f"✅ {node['title']} 连接成功", file=sys.stderr)
            else:
                print(f"❌ {node['title']} 连接失败", file=sys.stderr)
        nodes['data'] = valid_nodes

        # 5. 生成 Clash 配置
        print("\n正在生成 Clash 配置文件...", file=sys.stderr)
        clash_config = generate_clash_config(nodes)
        yaml_content = yaml.dump(clash_config, allow_unicode=True, sort_keys=False)

        # 6. 输出配置文件
        print("\n----- 生成的配置文件内容 -----", file=sys.stderr)
        print(yaml_content, file=sys.stderr)
        print("\n----- 配置文件生成完成 -----", file=sys.stderr)

        # 7. 保存配置文件
        config_path = 'clash_auto.yaml'
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
        print(f"\n配置文件已保存为: {config_path}", file=sys.stderr)

    except Exception as e:
        print(f"\n❌ 错误: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
