import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';


import { MessageService } from '../message.service';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { UserService } from '../user.service';
import { User } from '../user';

declare var usersBox: any;
declare var usersComponent: any;

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
    users$: Observable<any>;
    users: User[] = [];

    private page: number = 1;

    public sortByFields: any[] = [
        { fieldName: 'rating', humanReadableName: 'Рейтингу' },
        { fieldName: 'subscribers_count', humanReadableName: 'Количеству подписчиков' },
        { fieldName: 'comments_count', humanReadableName: 'Количеству комментариев' },
        { fieldName: 'posts_count', humanReadableName: 'Количеству постов' },
        { fieldName: 'hot_posts_count', humanReadableName: 'Количеству горячих постов' },
        { fieldName: 'pluses_count', humanReadableName: 'Количеству плюсов' },
        { fieldName: 'minuses_count', humanReadableName: 'Количеству минусов' },
        { fieldName: 'last_update_timestamp', humanReadableName: 'Времени последнего обновления' },
        { fieldName: 'next_updating_timestamp', humanReadableName: 'Периоду обновления' },
        { fieldName: 'username', humanReadableName: 'Никнейму' },
    ];

    // private searchText: string = '';
    // private sortBy: string = '';
    // private reverseSort: boolean = false;
    private searchParameters: any = {};

    constructor(
        private userService: UserService,
        private messageService: MessageService
    ) {

    }

    searchParametersChanged(searchParameters: any): void {
        this.searchParameters = searchParameters;
        this.resetTape();
        this.loadMore();
    }

    ngOnInit(): void {

    }


    loadMore() {
        this.userService.searchUsers(this.searchParameters, this.page).subscribe(result => {
            ++this.page;
            if (!result.results)
                return

            for (var user of result.results) {
                this.users.push(user);
            }

            if (!result.next) {
                this.messageService.info("Больше ничего нет");
                return;
            }

            if (usersBox.scrollHeight < usersComponent.scrollHeight + 500)
                setTimeout(() => this.loadMore(), 100);
        });
    }

    resetTape() {
        this.users = [];
        this.page = 1;
    }

    onScroll() {
        this.loadMore();
    }
}
