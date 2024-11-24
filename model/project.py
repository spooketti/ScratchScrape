from init import Base
import sqlalchemy as db

class Project(Base):
    __tablename__ = "Project"
    id = db.Column("id",db.Integer,primary_key=True)
    projectID = db.Column("projectID",db.String)
    title =db.Column("Title",db.String)
    description = db.Column("Description",db.String)
    author = db.Column("Author",db.String)
    createdOn = db.Column("CreatedOn",db.String)
