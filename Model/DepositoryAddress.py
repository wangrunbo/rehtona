# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, SmallInteger, Integer, String, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class DepositoryAddress(Base):
    __tablename__ = 'depository_addresses'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(100), nullable=False)
    postcode = Column(String(6), nullable=False)
    prefecture_id = Column(SmallInteger, ForeignKey('prefectures.id'), nullable=False)
    address1 = Column(Text, nullable=False)
    address2 = Column(Text, nullable=False)
    company = Column(Text, nullable=False)
    tel = Column(String(20), nullable=False)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = Column(Integer, ForeignKey('administrators.id'), nullable=True, server_default=None)

    prefecture = relationship('Prefecture', backref='depository_addresses')
    modifier = relationship('Administrator', backref='modified_depository_addresses')


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
