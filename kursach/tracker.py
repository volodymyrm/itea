import os
import datetime
import time
import smtplib
import threading
import logging

from peewee import *
from selenium import webdriver
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from jinja2 import Environment, FileSystemLoader
from flask import Flask


class Tracker:

    def __init__(self, url=os.environ.get('UT_WEBPAGE_URL', 'https://chromereleases.googleblog.com/')):
        self.webpage = url
        self.output = []

    @property
    def scan(self):
        driver = webdriver.Chrome('chromedriver.exe')
        # driver = webdriver.Chrome('./chromedriver')
        driver.get(self.webpage)
        post_title_xpath = "//div[@class='post']/h2/a"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, post_title_xpath))
            )
            posts = driver.find_elements_by_xpath("//div[@class='post']")
            ids = [x.get_attribute('data-id') for x in posts]
            titles = [x.find_element_by_xpath("./h2/a").text for x in posts]
            dates = [x.find_element_by_xpath("./div/div/span").text for x in posts]
            links = [x.find_element_by_xpath("./h2/a").get_attribute('href') for x in posts]

            for i in range(len(posts)):
                self.output.extend([{'title': titles[i], 'release_date': dates[i], 'link': links[i], 'postid': ids[i]}])
        finally:
            logger.info('Scan complete')
            driver.quit()
            return self.output


class Notifier:

    email_server = os.environ.get('UT_EMAIL_SERVER', 'smtp.gmail.com')
    email_port = os.environ.get('UT_EMAIL_PORT', 587)
    login = os.environ.get('UT_EMAIL_SENDER', 'pchelokoshka@gmail.com')
    password = os.environ.get('UT_EMAIL_SENDER_PWD', 'Fluxld29')
    receiver = os.environ.get('UT_EMAIL_RECEIVER', 'vovych007@gmail.com')

    @staticmethod
    def notify(data):
        sent_from = __class__.login
        to = __class__.receiver
        msg = MIMEMultipart()
        msg['From'] = sent_from
        msg['To'] = to
        msg['Subject'] = data['title']
        body = 'Attention!!! \n{title}\n{date}\n{link}'.format(title=data['title'],
                                                               date=data['release_date'],
                                                               link=data['link'])
        msg.attach(MIMEText(body, 'plain'))
        email_text = str(msg)
        try:
            server = smtplib.SMTP(__class__.email_server, __class__.email_port)
            server.starttls()
            server.login(__class__.login, __class__.password)
            server.sendmail(__class__.login, __class__.receiver, email_text)
            logger.info('Email to {r} sent successfully'.format(r=to))
        except Exception as e:
            logger.error(e)
        else:
            server.close()


class DataBase:

    DATABASE = os.environ.get('UT_DB_NAME', 'Update.db')
    database = SqliteDatabase(DATABASE)

    def __init__(self):
        self.create_tables()

    def create_tables(self):
        with self.database:
            self.database.create_tables([Update])

    def write_to_db(self, data):
        for item in data:
            if not item['postid'] in self.select_postid:
                try:
                    Notifier.notify(item)
                    query = (Update.insert(title=item['title'],
                                           release_date=item['release_date'],
                                           link=item['link'],
                                           postid=item['postid'],
                                           created=datetime.datetime.now())
                                   .on_conflict('replace')
                                   .execute())
                    logger.info('{i} added to database'.format(i=str(item)))
                except Exception as e:
                    logger.error(e)

    @property
    def select_postid(self):
        query = Update.select(Update.postid)
        posts = []
        for item in query:
            posts.extend([item.postid])
        return posts

    @property
    def select_all(self):
        query = Update.select()
        return query


class Update(Model):
    class Meta:
        database = DataBase.database

    postid = CharField()
    title = CharField()
    release_date = DateTimeField()
    link = CharField()
    created = DateTimeField()


def create_html(items):
    try:
        root = os.path.dirname(os.path.abspath(__file__))
        templates_dir = root
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('index_template.html')
        index = template.render(items=items)
    except Exception as e:
        logger.error(e)
    else:
        return index


def setup_custom_logger(name):
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(os.environ.get('UT_LOGFILE', 'logfile.log'), mode='a')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    if os.environ.get('UT_DEBUG'):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger


app = Flask(__name__)


@app.route('/', methods=['GET'])
def reader():
    logger.info('Database was queried')
    return create_html(db.select_all)


if __name__ == '__main__':
    logger = setup_custom_logger('UpdateTracker')
    t = Tracker()
    db = DataBase()
    threading.Thread(target=app.run).start()
    interval = os.environ.get('UT_DAYS_INTERVAL', 1)
    timeout = interval * 60 * 60 *24
    timer = timeout
    try:
        logger.info('Tracker run with {}d interval'.format(interval))
        print('Press CTRL+C to exit')
        output = t.scan
        db.write_to_db(output)
        while True:
            time.sleep(0.985)
            if timer > 0:
                timer -= 1
            else:
                output = t.scan
                db.write_to_db(output)
                timer = timeout
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt')
