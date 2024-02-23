from database_connection import DataBaseConnection
import datetime

db = DataBaseConnection(
    host="localhost",
    user="root",
    passwd="",
    database="tradetalkerdb"
)

'''
my_cursor = db.cursor()
my_cursor.execute("DESCRIBE Article")
for x in my_cursor:
    print(x)

my_cursor.execute("DESCRIBE User")
for x in my_cursor:
    print(x)

my_cursor.execute("INSERT INTO User (UserName, Email, Password, Preferences) VALUES (%s, %s, %s, %s)", ("hi", "acea@","hello", 123))
db.commit()
my_cursor.execute("SELECT * FROM User")
for x in my_cursor:
    print(x)

my_cursor.execute("SELECT * FROM Article")
for x in my_cursor:
    print(x)
'''
# USER
''' Test for user methods and usability template
db.user_insert_user("sh", "shsh", "shshsh", 123)
users = db.user_select_all()
for x in users:
    print(x)

output:
(1, 'Shayan4', 'Password3', 'shaya343n.brn@yahoo.com', 12345)
(2, 'qweq', 'Password3', 'shaya34qwe3n.brn@yahoo.com', 12345)
(3, 'try', 'Password3', 'new.brn@yahoo.com', 12345)
(4, 'ewgfhjdf;', 'Password3', 'new.bwfsergdrn@yahoo.com', 12345)
(6, 'hi', 'hello', 'acea@', 123)
(7, 'sh', 'shsh', 'shshsh', 123)
'''

# ARTICLE
'''
db.article_insert_article("test_article", "google", "hello world", "23/02/2024", "no url", "hi")
articles = db.article_select_all()
for x in articles:
    print(x)

output:
(9, 1, 'test_article', 'hello world', None, 'no url', '', 'hi', 0.0)
'''

#COMPANY
"""
db.company_insert_company("apple", "appl", 123.2, "tech", "apple tech company")
companies = db.company_select_all()
for x in companies:
    print(x)
output:
(1, 'google', 'ggl', None, 'tech', 'google tech company', None, None, None)
(2, 'microsoft', 'mcr', None, 'tech', 'michrosoft', None, None, None)
(3, 'apple', 'appl', 123.2, 'tech', 'apple tech company', None, None, None)


print(db.company_get_company_id_by_name("apple")[0])
# output: 3

db.company_update_stock_price("apple", 55)
db.company_update_predicted_stock_price("apple", 12)
db.company_update_sentiment_score("apple", 0.6)
db.company_update_stock_variance("apple", 1.5)
companies = db.company_select_all()
for x in companies:
    print(x)

output:
(3, 'apple', 'appl', 55.0, 'tech', 'apple tech company', 12.0, 1.5, 0.6)

print(db.company_select_by_name("google"))
# output : (1, 'google', 'ggl', None, 'tech', 'google tech company', None, None, None)
print(db.company_select_by_industry("tech"))
# output: [(1, 'google', 'ggl', None, 'tech', 'google tech company', None, None, None), (2, 'microsoft', 'mcr', None, 'tech', 'michrosoft', None, None, None), (3, 'apple', 'appl', 55.0, 'tech', 'apple tech company', 12.0, 1.5, 0.6)]
"""
#FOLLOW
"""
print(db.follow_check(1, 2))
db.follow_toggle(1, 2, "23/02/2024")
print(db.follow_check(1, 2))
db.follow_toggle(1, 2, "23/02/2024")
print(db.follow_check(1, 2))
output:
True
False
True


# db.follow_toggle(1, 2, "23/02/2024")
# db.follow_toggle(1, 3, "23/02/2024")
print(db.follow_select_all())
print(db.follow_get_user_following_companies(1))
output:
[(14, 1, 3, None), (15, 1, 2, None)]
[3, 2]
"""

#LIKETABLE
"""
print(db.like_relation_exists(1, 20))
False
db.toggle_like(1, 20)
print(db.like_relation_exists(1, 20))
True
db.toggle_like(1, 20)
print(db.like_relation_exists(1, 20))
False
"""

#BOOKMARK
"""
print(db.bookmark_relation_exists(1, 20))
False
db.toggle_bookmark(1, 20)
print(db.bookmark_relation_exists(1, 20))
True
db.toggle_bookmark(1, 20)
print(db.bookmark_relation_exists(1, 20))
Flase
"""

#FAQ
"""
db.faq_insert_faq("How many members our group has?", "Seven members.")
db.faq_insert_faq("How did you bond so well?", "With a trip to SHAG-FEST.")
for x in db.faq_select_all():
    print(x)
"""

#USERQUESTION
"""
#db.user_question_insert(1, "SUP?", datetime.datetime.now())
#db.user_question_insert(1, "YO?", datetime.datetime.now())
#db.user_question_insert(2, "What time is it?", datetime.datetime.now())

db.user_question_mark_answered(1)
user_q = db.user_question_select_all()
for x in user_q:
    print(x)
user_1_q = db.user_question_select_one_user_questions(1)
for x in user_1_q:
    print(x)
output:
(1, 1, 'SUP?', datetime.datetime(2024, 2, 23, 19, 20, 46), 1)
(2, 1, 'YO?', datetime.datetime(2024, 2, 23, 19, 20, 46), 0)
(3, 2, 'What time is it?', datetime.datetime(2024, 2, 23, 19, 20, 46), 0)
(1, 1, 'SUP?', datetime.datetime(2024, 2, 23, 19, 20, 46), 1)
(2, 1, 'YO?', datetime.datetime(2024, 2, 23, 19, 20, 46), 0)
"""

#ARTICLECOMMENT
"""
#db.article_comment_insert(1, 20, "nice?", datetime.datetime.now(), None)
#db.article_comment_insert(1, 21, "nice?", datetime.datetime.now(), None)
#db.article_comment_insert(1, 22, "nice?", datetime.datetime.now(), None)

#db.article_comment_insert(2, 22, "nice.", datetime.datetime.now(), 3)
ac = db.article_comment_select_all()
for x in ac:
    print(x)
(2, 1, 20, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(3, 1, 21, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(4, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(6, 1, 20, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(7, 1, 21, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(8, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(9, 2, 22, 'nice.', datetime.datetime(2024, 2, 23, 19, 57, 8), 3)
ac = db.article_comment_select_by_article(22)
for x in ac:
    print(x)
(4, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(8, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(9, 2, 22, 'nice.', datetime.datetime(2024, 2, 23, 19, 57, 8), 3)
ac = db.article_comment_select_by_user(1)
for x in ac:
    print(x)
(2, 1, 20, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(3, 1, 21, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(4, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 17), None)
(6, 1, 20, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(7, 1, 21, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)
(8, 1, 22, 'nice?', datetime.datetime(2024, 2, 23, 19, 56, 28), None)

"""

