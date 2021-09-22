from sqlalchemy.orm import registry, declarative_base, relationship, Session
from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, insert, select, update
from sqlalchemy import create_engine, text

mapper_registry = registry()
print(mapper_registry.metadata)
Base = declarative_base(())
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)


class User(Base):
    __tablename__ = 'user_account'
    id = Column(Integer, primary_key=True)
    name = Column(String(30)),
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"



Base.metadata.create_all(engine)
"""
insert
"""
squidward = User(name="zaoad", fullname="syeed abrar zaoad")
sakibusr = User(name="sakib", fullname="kazi tanjim shakib")
session = Session(engine)
session.add(squidward)
session.add(sakibusr)
print(session.new)
session.flush()
session.commit()
print('before update')
zaoad = session.execute(select(User).filter_by(id=1)).scalar_one()
print('zaoad', zaoad)
zaoad.fullname="md syeed abrar zaoad"
session.flush()
session.commit()
print(zaoad)
print(squidward.id)
print(sakibusr.id)
print('after update')
zaoad = session.execute(select(User).filter_by(id=1)).scalar_one()
print('zaoad', zaoad)
"""
update
"""
session.execute(
update(User).
where(User.id == 2).
values(fullname="Sandy Squirrel Extraordinaire")
)
session.commit()
sakib= session.execute(select(User).where(User.id == 2)).first()
print(sakib)
session.close()
# print(select(User))
# row = session.execute(select(User)).first()
# print(row)