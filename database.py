import pymysql


class DB():

    def __init__(self, ip, user, password, database, login_user):
        self.ip = ip
        self.user = user
        self.password = password
        self.database = database

        try:
            self.db = pymysql.connect(ip, user, password, database)
        except Exception as e:
            print('连接数据库失败')
        else:
            self.cursor = self.db.cursor()
            self.cursor.execute('SELECT uid,authCode FROM typecho_users WHERE name="%s";' % login_user)
            user_info = self.cursor.fetchone()
            self.user_uid = user_info[0]
            self.user_authCode = user_info[1]
            self.cursor.execute('SELECT value FROM typecho_options WHERE name="secret";')
            self.serect = self.cursor.fetchone()[0]