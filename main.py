from post import MAIN
import json


with open("mirrors.conf", 'r', encoding='utf-8') as f:
    user_dict =  json.loads(f.read())
    #print(user_dict)


class GetHTMLFailed(Warning):
    pass
def cut2html():
    import win32clipboard, re

    win32clipboard.OpenClipboard()
    try:
        data = win32clipboard.GetClipboardData(49388)
    except Exception as e:
        raise GetHTMLFailed('GET HTML from Clipboard FAILED!')
    else:
        win32clipboard.CloseClipboard()
        data = data.decode()
        source_url = re.search(r'SourceURL:(.+?)\n', data)
        source_url = source_url.group(1) if source_url else ''
        html = re.sub(r'^.+?(?=<html>)', '', data, flags=re.S)
        with open('demo.html','w', encoding='utf-8')as f:
            f.write(html)
        return source_url, html


def html2md(html):
    import html2text as ht
    text_maker = ht.HTML2Text()
    md = text_maker.handle(html)
    with open('demo.md','w', encoding='utf-8')as f:
        f.write(md)
    return md


def get_title(url):
    import urllib
    from bs4 import BeautifulSoup
    url = urllib.request.urlopen(url).read()
    html = BeautifulSoup(url)
    title = html.title.string if html.title else html.h1.string if html.h1 else html.h2.string if html.h2 else ''
    return title


if __name__ == '__main__':
    try:
        source_url, html = cut2html()
    except GetHTMLFailed:
        print('未能从剪切板获取到HTML数据')
    else:
        markdown = html2md(html)
        title = ''
        if source_url:
            markdown = '> 本文转载自：%s，版权归原作者所属哦~\n\n' % source_url + markdown
            title = get_title(source_url)
        else:
            markdown = '> 本文出处已不可考，如有侵权，请联系[iyzyi](kljxnn@gmail.com)删除，真的很抱歉呐~\n\n' + markdown
        title = title if title else '抱歉，自动化获取本文标题失败，谁家的程序能保证百分百不出错呢'
        MAIN(user_dict, title, markdown)
    
    '''
    title='tttt'
    with open('demo.md', 'r', encoding='utf-8')as f:
        markdown = f.read()
    MAIN(user_dict, title, markdown)
    '''