from main import db

class Task(db.Model):
    """This class represents the tasks table."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer)
    text = db.Column(db.String(511))
    marked = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, list_id, text, marked):
        """initialize with text and list_id."""
        self.list_id = list_id
        self.text = text
        self.marked = marked

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_list_id(list_id):
        return Task.query.filter_by(list_id=list_id)

    @staticmethod
    def get_by_id(task_id):
        return Task.query.get(task_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Task {},{}: {}>".format(self.id, self.list_id, self.text)

class List(db.Model):
    """This class represents the task lists table."""

    __tablename__ = 'lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(511))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, name):
        """initialize with name"""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return List.query.all()

    @staticmethod
    def get_by_id(list_id):
        return List.query.get(list_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<List {}: {}>".format(self.id, self.name)
