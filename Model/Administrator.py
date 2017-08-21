# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, Integer, SmallInteger, String, Text, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class Administrator(Base):
    __tablename__ = 'administrators'

    id = Column(Integer, primary_key=True)
    password = Column(String(100), nullable=False)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=False, unique=True)
    sex_id = Column(SmallInteger, ForeignKey('sex.id'), nullable=False, server_default='1')
    birthday = Column(DateTime, nullable=True)
    postcode = Column(String(6), nullable=True)
    address = Column(Text, nullable=True)
    tel = Column(String(20), nullable=True)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    sex = relationship('Sex', backref='administrators')


if __name__ == '__main__':
    from Config.datasource import Session, engine
    # noinspection PyUnresolvedReferences
    from Sex import Sex

    session = Session()

    Base.metadata.create_all(engine)
