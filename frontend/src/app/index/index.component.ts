import { Component, OnInit } from '@angular/core';
import {ApiConfig} from '../api.config';
import {ApiService} from '../api.service';

@Component({
    selector: 'app-index',
    templateUrl: './index.component.html',
    styleUrls: ['./index.component.css']
})
export class IndexComponent implements OnInit {
    number_of_users: any = '∞';
    number_of_updated_users: any = '∞';

    constructor(private api: ApiService) { }

    ngOnInit() {
        this.api.get(`${ApiConfig.API_URL}/index/counters`).subscribe(result => {
            result = result.data;
            this.number_of_users = result.number_of_users;
            this.number_of_updated_users = result.number_of_updated_users;
        });
    }
}
