import models
from restycorn.restycorn.postgresql_read_only_resource import PostgreSQLReadOnlyResource


def get_statistics_graph_item_resource(sqlalchemy_table):
    return PostgreSQLReadOnlyResource(
        sqlalchemy_table=sqlalchemy_table,
        fields=('timestamp as x', 'value as y',),
        id_field='timestamp',
        order_by=('timestamp',),
        filter_by={
            #
        },
        paginated=False,
    )
