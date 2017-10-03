from app import db

class Task(db.Model):
    """This class represents the tasks table."""

    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer)
    text = db.Column(db.String(511))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())

    def __init__(self, list_id, text):
        """initialize with text and list_id."""
        self.list_id = list_id
        self.text = text

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Task.query.all()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Task {},{}: {}>".format(self.id, self.list_id, self.text)
