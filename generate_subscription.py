import pyaes
import requests
import base64
import json
import pyaes
import binascii
from datetime import datetime
import sys # 导入 sys 模块

# 修改 banner 打印到 stderr
print(" \t\tH͜͡E͜͡L͜͡L͜͡O͜͡ \u0295͜͡O͜͡R͜͡L͜͡D͜͡ \u0295͜͡X͜͡T͜͡R͜͡A͜͡C͜͡T͜͡ \u0295͜͡S͜͡ \u0295͜͡N͜͡O͡D͡E͡", file=sys.stderr)
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟", file=sys.stderr)
print("Author : \u0399\u1d7c", file=sys.stderr)
print(f"Date \t : {datetime.today().strftime('%Y-%m-%d')}", file=sys.stderr)
print("Version: 1.0", file=sys.stderr)
print("𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟 𓆝 𓆟 𓆞 𓆟", file=sys.stderr)
print("\u0399\u1d7c:", file=sys.stderr)
print(r"""

⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠤⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡴⠁⠀⡰⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢀⡎⢀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀
⣀⠀⠀⠀⠀⠀⠀⡠⠬⡡⠬⡋⠀⡄⠀⠀⠀⠀⠀⠀⠀
⡀⠁⠢⡀⠀⠀⢰⠠⢷⠰⠆⡅⠀⡇⠀⠀⠀⣀⠔⠂⡂
⠱⡀⠀⠈⠒⢄⡸⡑⠊⢒⣂⣦⠄⢃⢀⠔⠈⠀⠀⡰⠁
⠀⠱⡀⠀⠀⡰⣁⣼⡿⡿⢿⠃⠠⠚⠁⠀⠀⢀⠜⠀⠀
⠀⠀⠐⢄⠜⠀⠈⠓⠒⠈⠁⠀⠀⠀⠀⠀⡰⠃⠀⠀⠀
⠀⠀⢀⠊⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠾⡀⠀⠀⠀⠀
⠀⠀⢸⣄⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⣀⡇⠀⠀⠀⠀
⠀⠀⠸⢸⣳⠦⣍⣁⣀⣀⣀⣀⣠⠴⠚⠁⠇⠀⠀⠀⠀
⠀⠀⠀⢳⣿⠄⠸⠢⠍⠉⠉⠀⠀⡠⢒⠎⠀⠀⠀⠀⠀
⠀⠀⠀⠣⣀⠁⠒⡤⠤⢤⠀⠀⠐⠙⡇⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠣⡀⡼⠀⠀⠈⠱⡒⠂⡸⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠑⢒⠁⠀⠀⠀⠀⠀⠀⠀
""", file=sys.stderr)


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


def f(g, d, e):
    h = pyaes.AESModeOfOperationCBC(d, iv=e)
    i = b''.join(h.decrypt(g[j:j+16]) for j in range(0, len(g), 16))
    return i[:-i[-1]]


j = requests.post(a, headers=b, data=c)

if j.status_code == 200:
    k = j.text.strip()
    l = binascii.unhexlify(k)
    m = f(l, d, e)
    n = json.loads(m)

    print("\n----- JSON 数据 (n['data'] 部分) -----") #  添加分隔符，方便查看
    for item in n['data']: # 遍历 n['data'] 并打印，如果 n 本身数据量不大，可以直接 print(n)
        print(item)
    print("----- JSON 数据打印结束 -----\n")


    ss_urls = []
    for o in n['data']:
        p = f"aes-256-cfb:{o['password']}@{o['ip']}:{o['port']}"
        q = base64.b64encode(p.encode('utf-8')).decode('utf-8')
        r = f"ss://{q}#{o['title']}"
        ss_urls.append(r)

    subscription_link_content = "\n".join(ss_urls)
    subscription_link_base64 = base64.b64encode(subscription_link_content.encode('utf-8')).decode('utf-8')
    subscription_link = f"ss://{subscription_link_base64}"

    #  仍然打印订阅链接到 stdout
    print(subscription_link)
else:
    print(f"请求失败，状态码: {j.status_code}", file=sys.stderr)
