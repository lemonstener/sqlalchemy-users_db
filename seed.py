from models import User, Post, Tag, PostTag, db
from app import app

db.drop_all()
db.create_all()

u1 = User(first_name='Kenny',last_name="Omega",image_url='https://www.wrestlezone.com/assets/uploads/2018/12/kenny-omega-getty-3.jpg')
u2 = User(first_name='Adam',last_name="Page",image_url='https://staticg.sportskeeda.com/editor/2020/02/6377c-15824073658116-800.jpg')
u3 = User(first_name='Britt',last_name="Baker",image_url='https://www.ewrestlingnews.com/wp-content/uploads/2020/05/Britt-Baker-1.jpg')
u4 = User(first_name='Tony',last_name='Khan')

p1 = Post(title='Hi',content='Hello',user_id=1)
p2 = Post(title='Bye',content='Goodbye',user_id=2)
p3 = Post(title='Heya',content='Ho ho ho',user_id=3)
p4 = Post(title='Again',content='Mwah',user_id=1)
p5 = Post(title='Whoops',content='My bad',user_id=2)
p6 = Post(title='DMD',content='The doctor is here',user_id=3)

t1 = Tag(name='Fun')
t2 = Tag(name='Sad')
t3 = Tag(name='Huh?')

pt1 = PostTag(post_id=1,tag_id=1)
pt2 = PostTag(post_id=2,tag_id=2)
pt3 = PostTag(post_id=3,tag_id=1)
pt4 = PostTag(post_id=3,tag_id=3)
pt5 = PostTag(post_id=4,tag_id=3)

db.session.add_all([u1,u2,u3,u4])
db.session.commit()
db.session.add_all([p1,p2,p3,p4,p5,p6])
db.session.commit()
db.session.add_all([t1,t2,t3])
db.session.commit()
db.session.add_all([pt1,pt2,pt3,pt4,pt5])
db.session.commit()