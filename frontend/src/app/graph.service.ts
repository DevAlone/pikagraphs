import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { ApiConfig } from './api.config';
import { ApiService } from './api.service';

const apiUrl = '/rest';


@Injectable()
export class GraphService {
    constructor(private api: ApiService) { }
    getGraph(type: string, id: string): Observable<any> {
        return this.api.get(`${ApiConfig.GRAPH_URL}/${type}/${id}`);
    }
}
