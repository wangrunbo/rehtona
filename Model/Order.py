# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, Integer, String, SmallInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String(100), nullable=False)
    postcode = Column(String(6), nullable=False)
    address = Column(Text, nullable=False)
    tel = Column(String(20), nullable=False)
    amazon_account = Column(String(30), nullable=False)
    total_price = Column(Integer, nullable=False)
    delivery_type_id = Column(SmallInteger, ForeignKey('delivery_types.id'), nullable=False)
    order_status_id = Column(SmallInteger, ForeignKey('order_statuses.id'), nullable=False, server_default='1')
    finish = Column(TIMESTAMP, nullable=True, server_default=None)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=True)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = Column(Integer, ForeignKey('administrators.id'), nullable=True, server_default=None)
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    user = relationship('User', backref='orders')
    delivery_type = relationship('DeliveryType', backref='orders')
    order_status = relationship('OrderStatus', backref='orders')
    post = relationship('Post', backref='order')
    modifier = relationship('Administrator', backref='modified_orders')


if __name__ == '__main__':
    from Config.datasource import Session
