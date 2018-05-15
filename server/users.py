import models
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource


users = PostgreSQLReadOnlyResource(
    sqlalchemy_table=models.core_user,
    fields=('id', 'username', 'info', 'avatar_url', 'rating', 'comments_count', 'posts_count', 'hot_posts_count',
            'pluses_count', 'minuses_count', 'last_update_timestamp', 'subscribers_count', 'is_rating_ban',
            'updating_period', 'is_updated', 'pikabu_id', 'gender', 'approved', 'awards', 'signup_timestamp',
            'deleted'),
    id_field='username',
    order_by=('id', 'rating', 'username', 'subscribers_count', 'comments_count', 'posts_count',
              'hot_posts_count', 'pluses_count', 'minuses_count', 'last_update_timestamp', 'updating_period',
              'pikabu_id', 'approved', 'signup_timestamp',),
    search_by=('username', ),
    filter_by={
        'username': ('=',),
        'rating': ('=', '>', '<'),
        'deleted': ('=', ),
    },
    page_size=50,
)


pikabu_users = PostgreSQLReadOnlyResource(
    sqlalchemy_table=models.core_pikabuuser,
    fields=('pikabu_id', 'username', 'is_processed'),
    id_field='pikabu_id',
    order_by=('pikabu_id', 'username', ),
    search_by=('username', ),
    filter_by={
        'pikabu_id': ('=', '>', '<'),
        'username': ('=', ),
        'is_processed': ('=',),
    },
    page_size=50,
)


def get_user_graph_item_resource(sqlalchemy_table):
    return PostgreSQLReadOnlyResource(
        sqlalchemy_table=sqlalchemy_table,
        fields=('timestamp as x', 'value as y',),
        id_field='id',
        order_by=('id',),
        filter_by={
            'user_id': ('=',),
        },
        paginated=False,
    )
