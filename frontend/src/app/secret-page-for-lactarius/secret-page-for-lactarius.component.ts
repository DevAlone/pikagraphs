import { Component, OnInit } from '@angular/core';
import {ApiConfig} from '../api.config';
import {ApiService} from '../api.service';

@Component({
    selector: 'app-secret-page-for-lactarius',
    templateUrl: './secret-page-for-lactarius.component.html',
    styleUrls: ['./secret-page-for-lactarius.component.css']
})
export class SecretPageForLactariusComponent implements OnInit {
    items: any[];
    data: string;
    constructor(private api: ApiService) { }

    ngOnInit() {
        this.api.get(`${ApiConfig.API_URL}/secret_page_for_lactarius`).subscribe(result => {
            this.items = result.data;
            console.log('got');
            console.log(result);
            console.log('asdfasdf');
            console.log(this.items);
            var data = "";
            for (const item of this.items) {
                data += item.time + " " + item.stories_count + " " + item.subscribers_count + "\n";
            }
            this.data = data;
        });
    }
}
