from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    relationship,
    backref
    )
from zope.sqlalchemy import ZopeTransactionExtension

pbbDBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
pbbBase = declarative_base()
