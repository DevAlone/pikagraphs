export class User
{
    name: string;
    info: string;
    avatar_url: string;
    rating: number;
    comments_count: number;
    posts_count: number;
    hot_posts_count: number;
    pluses_count: number;
    minuses_count: number;
    last_update_timestamp: number;
    subscribers_count: number;
    is_rating_ban: number;
    updating_period: number;

    public constructor(init?:Partial<any>) {
        Object.assign(this, init);
    }
};
