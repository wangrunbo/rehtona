# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, SmallInteger, Integer, String, TIMESTAMP
from Config.datasource import Base


class AmazonAccountStatus(Base):
    __tablename__ = 'amazon_account_statuses'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sort = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    STOPPED = 1  # 停止
    IDLE = 2  # 未使用
    USING = 3  # 使用中
    ERROR = 4  # 错误


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
    for amazon_account_status in session.query(AmazonAccountStatus).all():
        print(amazon_account_status.sort)
