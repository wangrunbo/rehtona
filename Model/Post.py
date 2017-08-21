# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, Integer, String, SmallInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)

    number = Column(String(13), nullable=False, unique=True)
    delivery_type_id = Column(SmallInteger, ForeignKey('delivery_types.id'), nullable=False)
    postage = Column(Integer, nullable=False)
    name = Column(String(100), nullable=False)
    postcode = Column(String(6), nullable=False)
    address = Column(Text, nullable=False)
    tel = Column(String(20), nullable=False)
    image = Column(String(20), nullable=False)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = Column(Integer, ForeignKey('administrators.id'), nullable=True, server_default=None)
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    delivery_type = relationship('DeliveryType', backref='posts')
    modifier = relationship('Administrator', backref='modified_posts')


if __name__ == '__main__':
    from Config.datasource import Session
    # noinspection PyUnresolvedReferences
    from AmazonAccountStatus import AmazonAccountStatus

    session = Session()
