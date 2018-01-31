import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs/Observable';
import { catchError, map, tap } from 'rxjs/operators';
import { of } from 'rxjs/observable/of';
import { ApiConfig } from './api.config';


@Injectable()
export class ApiService {
	constructor(private http: HttpClient) { }

	public get(url: string, params: any={}): Observable<any> {
		var url = url;

        if (Object.keys(params).length) {
            url += '?';
    		for (var key in params) {
    			url += `${key}=${params[key]}&`;
    		}
        }

        return this.http.get(url, ApiConfig.HTTP_OPTIONS).pipe(
            // tap(_ => console.log("")),
            catchError(this.handleError<any[]>('get', []))
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
