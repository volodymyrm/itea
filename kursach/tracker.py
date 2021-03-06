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


class Scanner:
    """
    Scanner class that can scan pre-defined web page and return parsed result 
    :param : page to be parsed. Environment variable 'UT_WEBPAGE_URL' by default
    :return : list of dicts
    """
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
        except Exception as e:
            logger.error(e)
        finally:
            logger.info('Scan complete')
            driver.quit()
            return self.output


class Notifier:
    """
    Notification class that can send emails with text data.
        email_server - sender smpt server. Environment variable 'UT_EMAIL_SERVER' by default
        email_port - sender smpt port. Environment variable 'UT_EMAIL_PORT' by default
        login - sender email account userbame. Environment variable 'UT_EMAIL_SENDER' by default
        password - sender email account password. Environment variable 'UT_EMAIL_SENDER_PWD' by default
        receiver - receiver email. Environment variable 'UT_EMAIL_RECEIVER' by default
    """
    email_server = os.environ.get('UT_EMAIL_SERVER', 'smtp.gmail.com')
    email_port = os.environ.get('UT_EMAIL_PORT', 587)
    login = os.environ.get('UT_EMAIL_SENDER')
    password = os.environ.get('UT_EMAIL_SENDER_PWD')
    receiver = os.environ.get('UT_EMAIL_RECEIVER')

    @staticmethod
    def notify(data):
        """
        Static method that send email
        :param data: txt data to be send
        """
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
    """
    Working with SQL light database implementation
        DATABASE - database file. Environment variable 'UT_DB_NAME'
    """
    DATABASE = os.environ.get('UT_DB_NAME', 'Update.db')
    database = SqliteDatabase(DATABASE)

    def __init__(self):
        self.create_tables()

    def create_tables(self):
        with self.database:
            self.database.create_tables([Update])

    def write_to_db(self, data):
        """
        Method which perform writing to DB only unique results and notify about them via email
        :param: data - list of dictionaries for writing to DB
        """
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
        """
        Method which queries post id's from database 
        :return: posts - list of post id's
        """
        query = Update.select(Update.postid)
        posts = []
        for item in query:
            posts.extend([item.postid])
        return posts

    @property
    def select_all(self):
        """
        Method which queries all info from database 
        :return: query - all database rows
        """
        query = Update.select()
        return query


class Update(Model):
    """
    Database model description class
    """
    class Meta:
        database = DataBase.database

    postid = CharField()
    title = CharField()
    release_date = DateTimeField()
    link = CharField()
    created = DateTimeField()


def create_html(items):
    """
    Function that generate html code based on jinja template
    :param: items - list to be displayed on html page
    :return: html code
    """
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
    """
    Function that setup logger
    :param: name - logger name
            
            If system variable UT_DEBUG set to True, logger will switch to debug mode 
    """
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)-8s %(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')
    handler = logging.FileHandler(os.environ.get('UT_LOGFILE', 'logfile.log'), mode='a')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    if os.environ.get('UT_DEBUG', True):
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    return logger


def create_app(database):
    """
    Function that create Flask application with defined database for querying
    :param: database - database object
    """
    app = Flask(__name__)
    app.config['database'] = database
    return app


def reader():
    """
    Flask function which perform database query and return html result page
    :return: 
    """
    logger.info('Database was queried')
    database = app.config['database']
    return create_html(database.select_all)


if __name__ == '__main__':
    """
    Main application loop. Runs infinitely with pre-set interval until keyboard interrupt
    """

    logger = setup_custom_logger('UpdateTracker')
    t = Scanner()
    db = DataBase()
#    app = create_app(db)
#    x = app.route('/', methods=['GET'])(reader) # Flask decorator for reader
#    threading.Thread(target=app.run).start()
    interval = os.environ.get('UT_DAYS_INTERVAL', 1)
    timeout = interval * 60 * 60 *24 # generate interval value in days
    timer = timeout
    try:
        logger.info('Tracker run with {}d interval'.format(interval))
        print('Press CTRL+C to exit')
        output = t.scan
        db.write_to_db(output)
        print('Last scan:', datetime.date.today())
        logger.info('Last scan: {}'.format(datetime.date.today()))
        while True:
            time.sleep(0.985)
            if timer > 0:
                timer -= 1
            else:
                output = t.scan
                db.write_to_db(output)
                print('Last scan:', datetime.date.today())
                logger.info('Last scan: {}'.format(datetime.date.today()))
                timer = timeout
    except KeyboardInterrupt:
        logger.info('Keyboard interrupt')
