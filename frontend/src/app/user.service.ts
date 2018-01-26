import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { catchError, map, tap } from 'rxjs/operators';
import { User } from './user';


const usersApiUrl = 'http://localhost:8000/rest/users';
const httpOptions = {
        headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};


@Injectable()
export class UserService {
    constructor(
        private http: HttpClient,
    ) {
        console.log("fucking constructor");
    }

    searchUsers(term: string, page: number=1): Observable<any> {
        if (!term.trim()) {
            return of([]);
        }

        return this.http.get(`${usersApiUrl}/?name=${term}&page=${page}`).pipe(
            tap(_ => console.log("search users")),
            catchError(this.handleError<User[]>('searchUsers', []))
        );
    }

    private handleError<T> (operation = 'operation', result?: T) {
        return (error: any): Observable<T> => {
            // TODO: send the error to remote logging infrastructure
            console.error(error); // log to console instead

            // TODO: better job of transforming error for user consumption
            // this.log(`${operation} failed: ${error.message}`);

            // Let the app keep running by returning an empty result.
            return of(result as T);
        };
    }
}
