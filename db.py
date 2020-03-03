import sqlite3

connect = None


def init():
    global connect

    def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    connect = sqlite3.connect('feed.db', check_same_thread=False)
    connect.row_factory = dict_factory

    # init user
    connect.execute("""
    CREATE TABLE IF NOT EXISTS user (
        id int primary key not null, 
        name char(30) not null
    )
    """)
    # init follow
    connect.execute("""
    CREATE TABLE IF NOT EXISTS follow (
        id int primary key not null, 
        user_id int not null,
        following int not null
    )
    """)
    connect.execute('CREATE INDEX IF NOT EXISTS follow_user_id on follow (user_id)')

    # init repo
    connect.execute("""
    CREATE TABLE IF NOT EXISTS repo (
        id int primary key not null, 
        user_id int not null,
        name char(30) not null,
        fork_from int not null default 0
    )
    """)
    connect.execute('CREATE INDEX IF NOT EXISTS repo_user_id on repo (user_id)')

    # init event
    connect.execute("""
    CREATE TABLE IF NOT EXISTS event (
        id int primary key not null, 
        user_id int not null,
        action int not null,
        object_id int not null,
        create_time int not null
    )
    """)
    connect.execute('CREATE INDEX IF NOT EXISTS event_user_id on event (user_id)')


def create_test_data():
    global connect
    sql = """
    INSERT INTO user VALUES (1, 'imxyb'), (2, 'guido'), (3, 'linus'), (4, 'unknown')
    """
    connect.execute(sql)

    sql = """
    INSERT INTO follow VALUES (1,1,2),(2,1,3),(3,1,4),(4,4,2)
    """
    connect.execute(sql)

    sql = """
    INSERT INTO repo VALUES (1,2,'python',0),(2,2,'linux',0),(3,4,'linux',2)
    """
    connect.execute(sql)

    # 四个事件
    # 1. guido创建了 python 仓库
    # 2. linux创建了 linux 仓库
    # 3. unknown fork了 linus的linux 仓库
    # 3. unknown following 了linus
    sql = """
    INSERT INTO event VALUES 
        (1,2,'create_repo',1,1583239321),
        (2,3,'create_repo',2,1583239322),
        (3,4,'fork_repo',3,1583239323),
        (4,4,'following',2,1583239323)
    """
    connect.execute(sql)
    connect.commit()


def get_user_feed(user_id, offset, limit):
    global connect

    c = connect.cursor()

    following = []
    for row in c.execute('select following from follow where user_id=%d' % (user_id)):
        following.append(row['following'])

    result = []
    for row in c.execute(
            'select * from event where user_id in (%s) limit %d,%d' %
            (','.join('?' * len(following)), offset, limit), following):
        result.append(row)
    c.close()
    return result


def get_user_feed_count(user_id):
    global connect

    c = connect.cursor()

    following = []
    for row in c.execute('select following from follow where user_id=%d' % user_id):
        following.append(row['following'])

    c.execute(
        'select count(*) as count from event where user_id in (%s)' %
        (','.join('?' * len(following))), following)
    result = c.fetchone()
    c.close()
    return result['count']


def get_users_detail(user_ids):
    c = connect.cursor()
    c.execute('select * from user where id in (%s)' % (','.join('?' * len(user_ids))), user_ids)
    result = c.fetchall()
    c.close()
    return result


def get_user_detail(user_id):
    c = connect.cursor()
    c.execute('select * from user where id=%d' % user_id)
    result = c.fetchone()
    c.close()
    return result


def get_repo_detail(repo_id):
    c = connect.cursor()
    c.execute('select * from repo where id=%d' % repo_id)
    result = c.fetchone()
    c.close()
    return result
