import models
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource


comments = PostgreSQLReadOnlyResource(
    sqlalchemy_table=models.comments,
    fields=(
        'id', 'parent_id', 'creation_timestamp', 'first_parsing_timestamp', 'last_parsing_timestamp', 'rating', 'story_id', 'user_id', 'author_username', 'is_hidden', 'is_deleted', 'is_author_community_moderator', 'is_author_pikabu_team', 'text'),
    id_field='id',
    order_by=(
        'id', 'parent_id', 'creation_timestamp', 'first_parsing_timestamp', 'last_parsing_timestamp', 'rating', 'story_id', 'user_id', 'author_username', 'is_hidden', 'is_deleted', 'is_author_community_moderator', 'is_author_pikabu_team', 'text'),
    search_by=(),
    filter_by={
        'id': ('=', '>', '<'),
        'parent_id': ('=', '>', '<'),
        'creation_timestamp': ('=', '>', '<'),
        'first_parsing_timestamp': ('=', '>', '<'),
        'last_parsing_timestamp': ('=', '>', '<'),
        'rating': ('=', '>', '<'),
        'story_id': ('=', '>', '<'),
        'user_id': ('=', '>', '<'),
        'author_username': ('=', ),
        'is_hidden': ('=', ),
        'is_deleted': ('=', ),
        'is_author_community_moderator': ('=', ),
        'is_author_pikabu_team': ('=', ),
    },
    page_size=50,
)

