# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, SmallInteger, Integer, String, TIMESTAMP
from Config.datasource import Base


class OrderStatus(Base):
    __tablename__ = 'order_statuses'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sort = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    CASHING = 1  # 未支付
    FINISH = 2  # 交易完成
    FAIL = 3  # 交易失败
    TIME_OUT = 4  # 交易超时


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
