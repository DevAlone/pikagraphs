import { Component, OnInit } from '@angular/core';
import { Community } from '../community';
import { CommunityService } from '../community.service';
import { MessageService } from '../message.service';

declare var communitiesBox: any;
declare var communitiesComponent: any;


@Component({
    selector: 'app-communities',
    templateUrl: './communities.component.html',
    styleUrls: ['./communities.component.css']
})
export class CommunitiesComponent implements OnInit {
    communities: Community[] = [];

    page: number = 1;

    public sortByFields: any[] = [
        { fieldName: 'subscribers_count', humanReadableName: 'Количеству подписчиков' },
        { fieldName: 'stories_count', humanReadableName: 'Количеству постов' },
        { fieldName: 'last_update_timestamp', humanReadableName: 'Времени последнего обновления' },
        { fieldName: 'name', humanReadableName: 'Названию' },
    ];

    private searchParams: any = {};

    constructor(
        private communitiesService: CommunityService,
        private messageService: MessageService,
    ) { }

    ngOnInit() {
    }

    searchParametersChanged(searchParameters: any): void {
        this.searchParams = searchParameters;

        this.resetTape();
        this.loadMore();
    }

    loadMore() {
        this.communitiesService.search(
                this.searchParams, this.page
        ).subscribe(result => {
            ++this.page;

            for (var community of result.results) {
                this.communities.push(community);
            }

            if (!result.next) {
                this.loadMore = () => {};
                this.messageService.info("Больше ничего нет");
                return;
            }

            if (communitiesBox.scrollHeight < communitiesComponent.scrollHeight + 500)
                setTimeout(() => this.loadMore(), 100);
        });
    }

    resetTape() {
        this.communities = [];
        this.page = 1;
    }

    onScroll() {
        this.loadMore();
    }
}
