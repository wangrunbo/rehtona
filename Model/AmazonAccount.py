# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, text, Integer, String, SmallInteger, Text, TIMESTAMP
from sqlalchemy.orm import relationship
from Config.datasource import Base


class AmazonAccount(Base):
    __tablename__ = 'amazon_accounts'

    id = Column(Integer, primary_key=True)
    email = Column(String(30), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    balance = Column(Integer, nullable=False, server_default='0')
    depository_address_id = Column(SmallInteger, ForeignKey('depository_addresses.id'), nullable=False)
    amazon_account_status_id = Column(SmallInteger, ForeignKey('amazon_account_statuses.id'), nullable=False, server_default='1')
    creator_id = Column(Integer, ForeignKey('administrators.id'), nullable=False)
    note = Column(Text, nullable=True, server_default=None)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    modifier_id = Column(Integer, ForeignKey('administrators.id'), nullable=True, server_default=None)

    depository_address = relationship('DepositoryAddress', backref='amazon_accounts')
    amazon_account_status = relationship('AmazonAccountStatus', backref='amazon_accounts')
    creator = relationship('Administrator', backref='created_amazon_accounts', foreign_keys=creator_id)
    modifier = relationship('Administrator', backref='modified_amazon_accounts', foreign_keys=modifier_id)


if __name__ == '__main__':
    from Config.datasource import Session
    # noinspection PyUnresolvedReferences
    from AmazonAccountStatus import AmazonAccountStatus
    from Administrator import Administrator
    from Sex import Sex

    session = Session()

    for amazon_account in session.query(AmazonAccount).all():
        print(amazon_account.email)
