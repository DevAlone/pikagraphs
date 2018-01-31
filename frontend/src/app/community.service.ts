import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Community } from './community';
import { ApiConfig } from './api.config';
import { ApiService } from './api.service';

import { map, filter, scan } from 'rxjs/operators';


@Injectable()
export class CommunityService {
	constructor(private api: ApiService) { }

	search(searchParams: any, page: number=1): Observable<any> {
		searchParams.page = page;

		return this.api.get(ApiConfig.COMMUNITIES_API_URL, searchParams);
    }
    getCommunityByUrlName(urlName: string): Observable<Community> {
    	return this.api.get(`${ApiConfig.COMMUNITY_API_URL}/${urlName}`).pipe(
    		map(result => new Community(result))
    	);
    }
}
