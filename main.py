from post import MAIN
import json


with open("mirrors.conf", 'r', encoding='utf-8') as f:
    user_dict =  json.loads(f.read())
    #print(user_dict)


def cut2html():
    from clipboard import GetHtmlAndSource
    source_url, html = GetHtmlAndSource()
    if html:
        if ord(html[-1]) == 0:
            html = html[:-1]
        #剪切板最后一个字符为\x00，转换成markdown时文章末尾依然含有\x00，上传到typecho时报500错误，数据库出错。
        with open('demo.html','w', encoding='utf-8')as f:
            f.write(html)
    return source_url, html


def html2md(html, source_url):
    import html2text
    text_maker = html2text.HTML2Text()
    md = text_maker.handle(html)
    if source_url:
        md = '> 本文转载自：%s，版权归原作者所属哦~\n\n' % source_url + md
    else:
        md = '> 本文出处已不可考，如有侵权，请联系[iyzyi](kljxnn@gmail.com)删除，真的很抱歉呐~\n\n' + md
    with open('demo.md','w', encoding='utf-8')as f:
        f.write(md)
    return md


def get_title(url):
    import urllib
    from bs4 import BeautifulSoup
    title = None
    if url:
        try:
            url = urllib.request.urlopen(url).read()
            html = BeautifulSoup(url, 'lxml')
            title = html.title.string if html.title else html.h1.string if html.h1 else html.h2.string if html.h2 else ''
        except Exception as e:
            title = None
            print('[*] Get title failed from url: %s' % e)
    title = title if title else '抱歉，自动化获取本文标题失败，谁家的程序能保证百分百不出错呢'
    return title


if __name__ == '__main__':
    source_url, html = cut2html()
    print(source_url)
    if html:
        markdown = html2md(html, source_url)
        title = get_title(source_url)
        print(title)
        MAIN(user_dict, title, markdown)
    else:
        print('未能从剪切板获取到HTML数据')
    '''
    title='tttt'
    with open('demo.md', 'r', encoding='utf-8')as f:
        markdown = f.read()
    MAIN(user_dict, title, markdown)
    '''