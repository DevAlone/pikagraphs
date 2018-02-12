import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Community } from './community';
import { ApiConfig } from './api.config';
import { ApiService } from './api.service';

import { map, filter, scan } from 'rxjs/operators';


@Injectable()
export class CommunityService {
    constructor(private api: ApiService) { }

    public search(searchParams: any, page: number= 0): Observable<any> {
        searchParams.page = page;

        return this.api.get(ApiConfig.COMMUNITIES_API_URL, searchParams);
    }
    public count(searchParams: any, page: number = 0): Observable<any> {
        searchParams = Object.assign({}, searchParams);
        searchParams.page = page;
        searchParams.count = true;
        return this.api.get(ApiConfig.COMMUNITIES_API_URL, searchParams);
    }
    public getCommunityByUrlName(urlName: string): Observable<any> {
        return this.api.get(`${ApiConfig.COMMUNITY_API_URL}/${urlName}`).pipe(
            map(result => new Community(result))
        );
    }
}
