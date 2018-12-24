import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs';


import { MessageService } from '../message.service';
import { ActivatedRoute, Router, Params } from '@angular/router';
import { UserService } from '../user.service';
import { User } from '../user';
import { LoadingAnimationService } from '../loading-animation.service';

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
    timers: any[] = [];
    subscriptions: any[] = [];
    count_subscription: any;
    count: any = 0;

    private page = 0;

    private searchParameters: any = {};

    constructor(
        private userService: UserService,
        private messageService: MessageService,
        private route: ActivatedRoute,
        private router: Router,
        private loadingAnimationService: LoadingAnimationService,
    ) {

    }

    searchParametersChanged(searchParameters: any): void {
        this.searchParameters = searchParameters;
        this.resetTape();
        this.loadMore();

        this.count = '-';
        if (this.count_subscription) {
            this.count_subscription.unsubscribe();
        }
        this.count_subscription = this.userService.count(this.searchParameters, 0).subscribe(result => {
            this.count = result.count;
        });
    }

    ngOnInit(): void {

    }

    loadMore() {
        this.loadingAnimationService.start();
        this.subscriptions.push(
          this.userService.search(this.searchParameters, this.page).subscribe(result => {
                this.loadingAnimationService.stop();
                ++this.page;

                if (!result.data.length) {
                  return;
                }

                for (const user of result.data) {
                    this.users.push(new User(user));
                }

                /*if (!result.next) {
                    return;
                }*/

                if (usersBox.scrollHeight < usersComponent.scrollHeight + 500) {
                    this.timers.push(setTimeout(() => this.loadMore(), 100));
                }
            })
        );
    }

    resetTape() {
        this.users = [];
        for (const timer of this.timers) {
            clearTimeout(timer);
        }

        for (const subscription of this.subscriptions) {
            subscription.unsubscribe();
            this.loadingAnimationService.stop();
        }


        this.timers = [];
        this.subscriptions = [];

        this.page = 0;
    }

    onScroll() {
        this.loadMore();
    }

    public sortByFields: any[] = [
        {
            fieldName: 'rating',
            humanReadableName: {
                sortBy: 'рейтингу',
                name: 'рейтинг',
            }
        },
        {
            fieldName: 'subscribers_count',
            humanReadableName: {
                sortBy: 'Количеству подписчиков',
                name: 'подписчиков',
            }
        },
        {
            fieldName: 'comments_count',
            humanReadableName: {
                sortBy: 'Количеству комментариев',
                name: 'комментариев',
            }
        },
        {
            fieldName: 'posts_count',
            humanReadableName: {
                sortBy: 'Количеству постов',
                name: 'постов',
            }
        },
        {
            fieldName: 'hot_posts_count',
            humanReadableName: {
                sortBy: 'Количеству горячих постов',
                name: 'горячих постов',
            }
        },
        {
            fieldName: 'pluses_count',
            humanReadableName: {
                sortBy: 'Количеству плюсов',
                name: 'плюсов',
            }
        },
        {
            fieldName: 'minuses_count',
            humanReadableName: {
                sortBy: 'Количеству минусов',
                name: 'минусов',
            }
        },
        {
            fieldName: 'last_update_timestamp',
            humanReadableName: {
                sortBy: 'Времени последнего обновления',
                name: 'Время последнего обновления',
            }
        },
        {
            fieldName: 'updating_period',
            humanReadableName: {
                sortBy: 'Периоду обновления',
                name: 'Период обновления',
            }
        },
        {
            fieldName: 'username',
            humanReadableName: {
                sortBy: 'Никнейму',
                name: 'Никнейм',
            }
        },
        {
            fieldName: 'pikabu_id',
            humanReadableName: {
                sortBy: 'ID в базе пикабу',
                name: 'ID в базе пикабу',
            }
        },
        {
            fieldName: 'approved',
            humanReadableName: {
                sortBy: 'Подтверждён',
                name: 'Подтверждён',
            }
        },
        {
            fieldName: 'signup_timestamp',
            humanReadableName: {
                sortBy: 'Дате регистрации',
                name: 'Дате регистрации',
            }
        },
    ];
}
