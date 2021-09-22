from sqlalchemy import MetaData, Table, Column, Integer, String, ForeignKey, insert, select
from sqlalchemy import create_engine, text

engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
metadata_obj = MetaData()
user_table = Table(
    "user_account",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)
print(user_table.c.keys())
address_table = Table(
    "address",
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)
metadata_obj.create_all(engine)
stmt = insert(user_table).values(id=1, name="zaoad")
print(stmt)
with engine.connect() as con:
    result = con.execute(stmt)
    con.commit()
    print(result.inserted_primary_key)
    result = con.execute(
        insert(user_table),
        [
            {'name': 'syeed'},
            {'name': 'abrar'}
        ]
    )
    con.commit()

""" 
Select Sql
"""
print("-----------------select-----------------------")
stmt = select(user_table)
print(stmt)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
stmt = select(user_table).where(user_table.c.name == "zaoad")
print(stmt)
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print('row', row)
"""
insert
"""
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt)
print('1st')
with engine.connect() as con:
    result = con.execute(stmt)
    con.commit()
    print(result.all())
insert_stmt = insert(address_table).returning(address_table.c.id, address_table.c.email_address)
print(insert_stmt)
print('2nd')
with engine.connect() as con:
    result = con.execute(stmt)
    con.commit()
    print(result.all())
select_stmt = select(user_table.c.id, user_table.c.name + "@aol.com")
insert_stmt = insert(address_table).from_select(
    ["user_id", "email_address"], select_stmt
)
print(insert_stmt.returning(address_table.c.id, address_table.c.email_address))
print('3rd')
with engine.connect() as con:
    result = con.execute(stmt)
    con.commit()
    print(result.all())
