import { DateUtils } from './date_utils';


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
    subscribers_count: number;
    is_rating_ban: number;
    updating_period: number;
    is_updated: boolean;
    
    pikabu_id: number;
    gender: string;
    approved: string;
    awards: string;
    communities: string;
    _last_update_timestamp: number;
    _signup_timestamp: any;

    get signup_timestamp(): any {
        return DateUtils.timestampToDateString(this._signup_timestamp);
    }

    set signup_timestamp(value: any) {
        this._signup_timestamp = value;
    }

    get last_update_timestamp(): any {
        return DateUtils.timestampToDateString(this._last_update_timestamp);
    }

    set last_update_timestamp(value: any) {
        this._last_update_timestamp = value;
    }

    public constructor(init?:Partial<any>) {
        Object.assign(this, init);
    }
};