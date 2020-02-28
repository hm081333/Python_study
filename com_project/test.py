#!/usr/bin/env python
# Encoding: UTF-8
import sys
import urllib.request
import re

from tool import Args


def exit_program(exit_code):
    input("按下回车键退出")
    sys.exit(exit_code)
    pass


args_tool = Args(
    prog='抓取百度收录数量',
    description='抓取百度收录数量',
).add_param(
    "-h",
    "--help",
    action="help",
    help="显示帮助信息并退出"
).add_param(
    "-v",
    "--version",
    # 操作类型，版本号，打印后会自动退出程序
    action="version",
    # 打印的信息
    version="%(prog)s" + "\tv" + '1.0.0' + "\t构建于\t" + '2019/07/31',
    help="显示版本"
).add_param(
    "-s",
    "--site",
    dest="site",
    metavar="站点地址",
    help="站点地址（域名） 必填"
)

site = args_tool.get_args('site')

url = r'http://www.baidu.com/s?wd=site:' + site
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': 'BIDUPSID=7DD2D28A9FBEDBA3BDA02C3A9FC9E903;'
              'BAIDUID=7DD2D28A9FBEDBA3BDFF71E552C56B8B:FG=1;',
}

request = urllib.request.Request(
    url=url,
    headers=headers
)
response = urllib.request.urlopen(request)
html_content = response.read().decode('utf-8')
# print(html_content)
pattern = r'该网站共有(.*)<b(.*)>(.*)</b>$'
matchObj = re.search(pattern, html_content, flags=re.M | re.S | re.I)
# print(matchObj)
# print(matchObj.group(3))
recordCount = matchObj.group(3)
print(format(recordCount))
exit_program(0)
