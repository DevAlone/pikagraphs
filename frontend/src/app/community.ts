export class Community {
	url_name: string;
    name: string;
    description: string;
    avatar_url: string;
    background_image_url: string;
    subscribers_count: number;
    stories_count: number;
    last_update_timestamp: number;

	public constructor(init?:Partial<any>) {
		Object.assign(this, init);
	}


    get simplified_description(): string {
    	return this.description.replace(/<br>/g, '');
    }
}
