import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { User } from './user';
import { ApiConfig } from './api.config';
import { ApiService } from './api.service';


@Injectable()
export class UserService {
    constructor(
        private api: ApiService,
    ) {

    }

    searchUsers(searchParameters: any, page: number=0): Observable<any> {
        searchParameters.page = page;
        return this.api.get(ApiConfig.USERS_API_URL, searchParameters);
    }
    getUserByName(username: string): Observable<any> {
        return this.api.get(`${ApiConfig.USER_API_URL}/${username}`);
    }
}
