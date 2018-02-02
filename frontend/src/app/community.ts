import { DateUtils } from './date_utils';


export class Community {
	url_name: string;
    name: string;
    description: string;
    avatar_url: string;
    background_image_url: string;
    subscribers_count: number;
    stories_count: number;
    _last_update_timestamp: number;

    get last_update_timestamp(): any {
        return DateUtils.timestampToDateString(this._last_update_timestamp);
    }

    set last_update_timestamp(value: any) {
        this._last_update_timestamp = value;
    }

	public constructor(init?:Partial<any>) {
		Object.assign(this, init);
	}


    get simplified_description(): string {
    	return this.description.replace(/<br>/g, '');
    }
}
