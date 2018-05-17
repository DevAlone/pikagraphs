from bot.module import Module


class StatisticsModule(Module):
    processing_period = 60

    def __init__(self):
        super(StatisticsModule, self).__init__('statistics_module')

    async def _process(self):
        async with self.pool.acquire() as connection:
            await connection.execute(
                """
                WITH constants (curr_timestamp) AS (
                    VALUES (extract(epoch from now())::int)
                ) INSERT INTO statistics_users_in_queue_counts (timestamp, value)
                SELECT 
                    constants.curr_timestamp, 
                    (
                        SELECT COUNT(*) FROM core_user 
                        WHERE 
                            is_updated = true 
                            and last_update_timestamp <= constants.curr_timestamp - updating_period
                    )
                
                FROM constants
                ON CONFLICT (timestamp) DO NOTHING;
                """
            )
