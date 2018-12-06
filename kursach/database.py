from tracker import Notifier


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
                Notifier.notify(item)
                query = (Update.insert(title=item['title'],
                                       release_date=item['release_date'],
                                       link=item['link'],
                                       postid=item['postid'],
                                       created=datetime.datetime.now())
                               .on_conflict('replace')
                               .execute())

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
        for item in query:
            print(item)
        return query


class Update(Model):
    class Meta:
        database = DataBase.database

    postid = CharField()
    title = CharField()
    release_date = DateTimeField()
    link = CharField()
    created = DateTimeField()