from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True, future=True)
with engine.connect() as con:
    result = con.execute(text("select 'hello world'"))
    print(result.all())
    print('------------------')
    con.execute(text("create table student(x int, y int)"))
    con.execute(
        text("insert into student(x, y) values (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 2}, {"x": 3, "y": 3}]
    )
    result = con.execute(text("select * from student"))
    for x, y in result:
        print(x,y)
    for dict_row in result:
        x = dict_row['x']
        y = dict_row['y']
        print(x, y)

    # for row in result:
    #     y = row.y
    #
    #     # illustrate use with Python f-strings
    #     print(f"Row: {row.x} {row.y}")
    # print(result)
    # print(result.all())
    con.commit()
stmt = text("SELECT x, y FROM student ")
with Session(engine) as session:
    # con.execute(text("create table student(x int, y int)"))
    # con.execute(
    #     text("insert into student(x, y) values (:x, :y)"),
    #     [{"x": 1, "y": 1}, {"x": 2, "y": 2}, {"x": 3, "y": 3}]
    # )
    result = session.execute(stmt)
    for row in result:
        print(f" v2 x: {row.x}  y: {row.y}")