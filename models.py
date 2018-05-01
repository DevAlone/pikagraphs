from sqlalchemy import Table, Column, BigInteger, String, Integer, Boolean, MetaData

metadata = MetaData()


core_user = Table(
    'core_user', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('username', String),
    Column('info', String),
    Column('avatar_url', String),
    Column('rating', Integer),
    Column('comments_count', Integer),
    Column('posts_count', Integer),
    Column('hot_posts_count', Integer),
    Column('pluses_count', Integer),
    Column('minuses_count', Integer),
    Column('last_update_timestamp', BigInteger),
    Column('subscribers_count', Integer),
    Column('is_rating_ban', Boolean),
    Column('updating_period', Integer),
    Column('is_updated', Boolean),
    Column('pikabu_id', BigInteger),
    Column('gender', String(1)),
    Column('approved', String),
    Column('awards', String),
    Column('signup_timestamp', BigInteger),
    Column('deleted', Boolean),
)


def generate_graph_item_table(table_name):
    return Table(
        table_name, metadata,
        Column('id', BigInteger, primary_key=True),
        Column('user_id', BigInteger),
        Column('timestamp', BigInteger),
        Column('value', Integer),
    )


core_userratingentry = generate_graph_item_table('core_userratingentry')
core_usersubscriberscountentry = generate_graph_item_table('core_usersubscriberscountentry')
core_usercommentscountentry = generate_graph_item_table('core_usercommentscountentry')
core_userpostscountentry = generate_graph_item_table('core_userpostscountentry')
core_userhotpostscountentry = generate_graph_item_table('core_userhotpostscountentry')
core_userplusescountentry = generate_graph_item_table('core_userplusescountentry')
core_userminusescountentry = generate_graph_item_table('core_userminusescountentry')

communities_app_community = Table(
    'communities_app_community', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('url_name', String),
    Column('name', String),
    Column('description', String),
    Column('avatar_url', String),
    Column('background_image_url', String),
    Column('subscribers_count', Integer),
    Column('stories_count', Integer),
    Column('last_update_timestamp', BigInteger),
)

communities_app_communitycountersentry = Table(
    'communities_app_communitycountersentry', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('timestamp', BigInteger),
    Column('community_id', BigInteger),
    Column('subscribers_count', Integer),
    Column('stories_count', Integer),
)


pikabu_new_year_18_game_app_scoreboardentry = Table(
    'pikabu_new_year_18_game_app_scoreboardentry', metadata,
    Column('id', BigInteger, primary_key=True),
    Column('parse_timestamp', BigInteger),
)


pikabu_new_year_18_game_app_topitem = Table(
    'pikabu_new_year_18_game_app_topitem', metadata,
    Column('score_entry_id', BigInteger),
)


pikabu_new_year_18_game_app_scoreentry = Table(
    'pikabu_new_year_18_game_app_scoreentry', metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String),
    Column('avatar_url', String),
    Column('score', Integer),
    Column('date', String),
    Column('scoreboard_entry_id', Integer),
)


core_pikabuuser = Table(
    'core_pikabuuser', metadata,
    Column('pikabu_id', Integer, primary_key=True),
    Column('username', String),
    Column('is_processed', Boolean),
)
