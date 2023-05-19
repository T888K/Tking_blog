import re
import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0",
}

def get_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip
    ip = request.META.get('REMOTE_ADDR')
    return ip


def get_addr_info(ip):
    if ip.startswith('10.') or ip.startswith('192') or ip.startswith('127'):
        return '中国大陆'
    url = f'https://www.ip138.com/iplookup.php?ip={ip}&action=2'
    res = requests.get(url=url, headers=headers).content.decode('UTF-8')
    addr = re.findall(r'<td><span>(.*?)</span></td>', res, re.S)[0]
    print(addr)
    return addr



if __name__ == '__main__':
    get_addr_info('59.51.228.249')
    get_addr_info('106.13.185.190')
    get_addr_info('120.228.2.238')
    get_addr_info('127.0.0.1')



