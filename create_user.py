import sys
import asyncio
from bot.db import DB


async def main():
    username = sys.argv[1]
    db = DB.get_instance()
    pool = await db.get_pool()
    async with pool.acquire() as connection:
        await connection.execute('''
            INSERT INTO core_user 
                (username, rating, comments_count, posts_count, hot_posts_count, pluses_count, minuses_count, 
                 subscribers_count, is_rating_ban, updating_period, avatar_url, info, is_updated, 
                 last_update_timestamp, approved, awards, gender, pikabu_id, signup_timestamp, deleted)     
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, $20)
            ON CONFLICT (username) DO NOTHING;
        ''', username, 0, 0, 0, 0, 0, 0, 0, False, 1, '', '', True, 0, '', '', '-', None, 0, False)


if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
