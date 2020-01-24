import requests, re, os
from database import DB
from img import IMG



def md5(string):
    import hashlib
    m = hashlib.md5()
    m.update(bytes(string, 'utf-8'))
    return str(m.hexdigest()).lower()


def url_encode(string):
    from urllib.parse import quote
    return quote(string, 'utf-8')


class POST():

    def __init__(self, url, ip, user, password, database, login_user, login_password):
        self.host_url = url
        self.ip = ip
        self.user=user 
        self.password = password
        self.database = database
        self.login_user = login_user
        self.login_password = login_password
        self.session = requests.Session()
        #self.session_login = requests.Session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',}
        self.proxies = {'http':'127.0.0.1:8080','https': '127.0.0.1:8080'}
        self.login()

    
    def join_token(self, token4):
        token = self.token1 + '&' + self.token2 + '&' + self.token3 + '&' + token4
        token = md5(token)
        return token


    def login(self):
        #print('####登录后台中####')
        self.db = DB(self.ip, self.user, self.password, self.database, self.login_user)    
        self.token1 = str(self.db.serect)
        token4 = '{}/admin/login.php?referer={}%2Fadmin%2F'.format(self.host_url, url_encode(self.host_url))
        token = md5(self.token1 + '&' + token4)
        url = self.host_url + '/index.php/action/login?_=%s' % token
        data = {
            'name': self.login_user,
            'password': self.login_password,
            'referer': '{}%2Fadmin%2F'.format(url_encode(self.host_url))
            }
        self.headers['Referer'] = token4
        self.session.post(url, data, headers=self.headers)
        #print('Cookies:', self.session.cookies.get_dict())

        self.db = DB(self.ip, self.user, self.password, self.database, self.login_user)   
        self.token1 = str(self.db.serect)
        self.token2 = str(self.db.user_authCode)
        self.token3 = str(self.db.user_uid)

    
    def check_post(self, response):
        import urllib
        from bs4 import BeautifulSoup
        html = BeautifulSoup(response, 'lxml')
        title = html.title.string
        if re.match(r'\d{3}', html.title.string):
            return int(html.title.string)
        else:
            return 200


    def write_post(self, title, text, cid='', mid='', date='', attachment=()):
        #zprint('####上传文本####')
        token = self.join_token(r'{}/admin/write-post.php'.format(self.host_url))
        url = self.host_url + '/index.php/action/contents-post-edit?_=%s' % token
        if mid == '':
            self.db.cursor.execute('SELECT value FROM typecho_options WHERE name="defaultCategory";')
            mid = self.db.cursor.fetchone()[0]
        data = {
            'title': title,
            'text': text,
            #'fields[thumbnail]': img_url,
            #'fields[previewContent]': preview,
            #'fields[showTOC]': h2h3,
            'cid': cid,
            'do': 'publish',
            'markdown': '1',
            'date': date,
            'category[]': mid,
            'tags': '',
            'visibility': 'publish',
            'password': '',
            'allowComment': '1',
            'allowPing': '1',
            'allowFeed': '1',
            'trackback': '',
            'attachment[]': attachment,     #元组形式
            'timezone': '28800'
            }
        self.headers['Referer'] = r'{}/admin/write-post.php'.format(self.host_url)
        r = self.session.post(url, data, headers=self.headers)#, proxies=self.proxies)
        #print(r.content)
        flag = self.check_post(r.content)
        if flag == 200:
            print('发送成功')
        else:
            print('发送失败，错误码%s' % flag)


    def upload_attachment(self, pic_path, name='', cid=''):    
        '''
        return img{'url': %s, 'cid': %d}
        PS: name要带后缀，否则上传失败
        '''
        #print('####正在上传%s####'%pic_path)
        if name == '':
            name = os.path.split(pic_path)[1]
        name = url_encode(name)
        token = self.join_token(r'{}/admin/write-post.php'.format(self.host_url))
        if cid == '':
            url = self.host_url + '/index.php/action/upload?_=%s' % token
        else:
            url = self.host_url + '/index.php/action/upload?cid=%d&_=%s' % (cid, token)
        data = {'name': name}
        files = {'file': (name, open(pic_path, 'rb'))}
        self.headers['Referer'] = r'{}/admin/write-post.php'.format(self.host_url)
        r = self.session.post(url, data, files=files, headers=self.headers)
        img = {
            'url': r.json()[0],
            'cid': r.json()[1]['cid']
        }
        return img



def MAIN(user_dict, title, text):
    url = user_dict['url']
    ip = user_dict['ip']
    user = user_dict['user']
    password = user_dict['password']
    database = user_dict['database']
    login_user = user_dict['login_user']
    login_password = user_dict['login_password']
    cache_path = user_dict['cache_path']

    db = DB(ip, user, password, database, login_user)
    post = POST(url, ip, user, password, database, login_user, login_password)

    #try:
    img = IMG(post, text, url, cache_path)
    img_list = img.get_upload_img_list()
    text = img.img_sub()
    #except Exception as e:
    #    raise RuntimeError('图片正则替换出错！')
    attachment = tuple([img['cid'] for img in img_list])
    return post.write_post(title, text, attachment=attachment)
