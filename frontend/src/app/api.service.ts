import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable ,  of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';
import { ApiConfig } from './api.config';
import {MessageService} from './message.service';


@Injectable()
export class ApiService {
    constructor(
        private messageService: MessageService,
        private http: HttpClient
    ) { }
    public get(url: string, params: any = {}): Observable<any> {
        if (Object.keys(params).length) {
            url += '?';
            for (const key in params) {
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
              this.messageService.error(error.message);

              // Let the app keep running by returning an empty result.
              return of(result as T);
          };
      }
}
