import models
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource

communities = PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.communities_app_community,
        fields=('id', 'url_name', 'name', 'description', 'avatar_url', 'background_image_url', 'subscribers_count',
                'stories_count', 'last_update_timestamp'),
        id_field='url_name',
        order_by=('id', 'subscribers_count', 'name', 'stories_count', 'last_update_timestamp', ),
        search_by=('url_name', 'name', 'description',),
        page_size=50,
    )


def get_community_graph_item_resource(resource_name):
    return PostgreSQLReadOnlyResource(
        sqlalchemy_table=models.communities_app_communitycountersentry,
        fields=('timestamp as x', '{} as y'.format(resource_name)),
        id_field='community_id',
        order_by=('id',),
        filter_by={
            'community_id': ('=',),
        },
        paginated=False,
    )
