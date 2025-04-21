from App.database import db
from .faculty import Faculty
import os,string, random
from werkzeug.utils import secure_filename

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())

    def __init__(self, file):
        self.filename = self.store_file(file)

    def random_string():
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))

    def remove_file(filename):
        try:
            os.remove(os.path.join('App/reports', filename))
        except:
            print('file already Deleted')
    
    def get_url(self):
        return f'/reports/{self.filename}'
    
    def store_file(self, file):
        extension = os.path.splitext(file.filename)[1]
        newname = secure_filename(self.random_string() + extension)
        file.save(os.path.join('reports', newname))
        return newname
