# -*- coding: utf-8 -*-
from sqlalchemy import Column, text, SmallInteger, Integer, String, TIMESTAMP
from Config.datasource import Base


class DeliveryType(Base):
    __tablename__ = 'delivery_types'

    id = Column(SmallInteger, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    sort = Column(Integer, nullable=False, unique=True)
    created = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated = Column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    deleted = Column(TIMESTAMP, nullable=True, server_default=None)

    EMS = 1  # EMS
    AIR = 2  # 空运
    SAL = 3  # SAL
    SEA = 4  # 海运


if __name__ == '__main__':
    from Config.datasource import Session

    session = Session()
