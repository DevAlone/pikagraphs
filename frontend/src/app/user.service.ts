import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiConfig } from './api.config';
import { ApiService } from './api.service';


@Injectable()
export class UserService {
    constructor(
        private api: ApiService,
    ) {

    }

    public search(searchParameters: any, page: number = 0): Observable<any> {
        searchParameters.page = page;
        return this.api.get(ApiConfig.USERS_API_URL, searchParameters);
    }
    public count (searchParameters: any, page: number = 0): Observable<any> {
        searchParameters = Object.assign({}, searchParameters);
        searchParameters.page = page;
        searchParameters.count = true;
        return this.api.get(ApiConfig.USERS_API_URL, searchParameters);
    }
    public getUserByName(username: string): Observable<any> {
        return this.api.get(`${ApiConfig.USER_API_URL}/${username}`);
    }
}
