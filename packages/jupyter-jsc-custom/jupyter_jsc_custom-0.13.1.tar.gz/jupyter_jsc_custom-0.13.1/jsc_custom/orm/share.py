from jupyterhub.orm import Base
from jupyterhub.orm import JSONDict
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Unicode


class JSONDictCache(JSONDict):
    cache_ok = True


class UserOptionsShares(Base):
    """User Options Shares"""

    __tablename__ = "useroptions_shares"
    id = Column(Integer, primary_key=True, autoincrement=True)
    share_id = Column(Unicode(255), unique=True)
    user_options = Column(JSONDictCache, default={})

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.share_id}: {self.user_options}>"

    @classmethod
    def find(cls, db, user_options):
        """Find a group by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.user_options == user_options).first()

    @classmethod
    def find_by_share_id(cls, db, share_id):
        """Find a group by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.share_id == share_id).first()
