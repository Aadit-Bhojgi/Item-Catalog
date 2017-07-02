from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exists
from sports_database import Categories, Base, LatestItem, User

engine = create_engine('sqlite:///sports_database.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()
value = 'Soccer Ball'
item = session.query(LatestItem).filter_by(title=value).count()
print item

'''i = session.query(LatestItem).order_by(LatestItem.created_at.desc()).limit(14)
for p in i:
    print p.created_at
for i in range(1, 10):
    p = session.query(Categories).filter_by(id=i).one()
    print p.name
    print p.description_cat
    q = session.query(LatestItem).filter_by(category_id=i)
    for j in q:
        print '-', j.title
        print '--', j.description'''
