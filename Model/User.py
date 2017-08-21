# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, Integer, SmallInteger, String, Text, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    uid = Column(String(12), nullable=False, unique=True)
    username = Column(String(100), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    target_email = Column(String(100), nullable=True)
    password = Column(String(100), nullable=False)
    secret_key = Column(String(255), nullable=False, unique=True)
    tel_cert_code = Column(String(6), nullable=True)
    name = Column(String(100), nullable=True)
    sex_id = Column(Integer, ForeignKey('sex.id'), nullable=False, server_default='1')
    birthday = Column(DateTime, nullable=True)
    postcode = Column(String(6), nullable=True)
    address = Column(Text, nullable=True)
    tel = Column(String(20), nullable=True)
    user_status_id = Column(SmallInteger, ForeignKey('user_statuses.id'), nullable=False)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = Column(Integer, ForeignKey('administrators.id'), nullable=True, server_default=None)

    sex = relationship('Sex', backref='users')
    user_status = relationship('UserStatus', backref='users')
    modifier = relationship('Administrator', backref='modified_users')


if __name__ == '__main__':
    from Config.datasource import Session, engine
    # noinspection PyUnresolvedReferences
    from Sex import Sex

    session = Session()
