from init import Base
import sqlalchemy as db

class User(Base):
    __tablename__ = "Users"
    id = db.Column("id",db.Integer,primary_key=True)
    userID = db.Column("userID",db.String)
    profileID = db.Column("profileID",db.String)
    username =db.Column("Username",db.String)
    scratchteam = db.Column("ScratchTeam",db.Boolean)
    joinDate = db.Column("joinDate",db.String)
    status = db.Column("Status",db.String)
    bio = db.Column("Bio",db.String)
    country = db.Column("Spain",db.String)
    
    
