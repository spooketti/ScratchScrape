from init import Base
import sqlalchemy as db

class User(Base):
    __tablename__ = "Users"
    id = db.Column("id",db.Integer,primary_key=True)
    profileID = db.Column("Profile ID",db.String)
    username =db.Column("Username",db.String,unique=True)
    scratchteam = db.Column("Scratch Team",db.Boolean)
    joinDate = db.Column("Join Date",db.String)
    status = db.Column("Status",db.String)
    bio = db.Column("Bio",db.String)
    country = db.Column("Country",db.String)
    
    
