export class User
{
    username: string;
    info: string;
    avatar_url: string;
    rating: number;
    comments_count: number;
    posts_count: number;
    hot_posts_count: number;
    pluses_count: number;
    minuses_count: number;
    next_update_timestamp: number;
    last_update_timestamp: number;
    subscribers_count: number;
    is_rating_ban: number;
    updating_period: number;
    is_updated: boolean;
    
    pikabu_id: number;
    gender: string;
    approved: string;
    awards: string;
    communities: string;
    signup_timestamp: number;

    public constructor(init?:Partial<any>) {
        Object.assign(this, init);
    }
};