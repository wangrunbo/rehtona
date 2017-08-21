# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, SmallInteger, Integer, String, TIMESTAMP
from Config.datasource import Base


class UserStatus(Base):
    __tablename__ = 'user_statuses'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sort = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    INACTIVE = 1  # 未激活
    GENERAL = 2  # 一般会员
    LOCKED = 3  # 锁定
    DELETED = 4  # 删除


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
