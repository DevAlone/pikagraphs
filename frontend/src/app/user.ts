import { DateUtils } from './date_utils';


export class User
{
    id: number;
    username: string;
    info: string;
    _avatar_url: string;
    get avatar_url(): string {
        if (!this._avatar_url)
            return "https://cs.pikabu.ru/images/def_avatar/def_avatar_96.png";
        
        return this._avatar_url;
    }
    set avatar_url(value: string) {
        this._avatar_url = value;
    }
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