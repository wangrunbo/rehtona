# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, SmallInteger, Integer, String, TIMESTAMP
from Config.datasource import Base


class Sex(Base):
    __tablename__ = 'sex'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sort = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    NOT_SET = 1  # 未设定
    MALE = 2  # 男性
    FEMALE = 3  # 女性


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
