import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { ApiConfig } from '../api.config';

declare var newYear2018GameComponent: any;
declare var scoreboardsContainer: any;
declare var topContainer: any;


@Component({
	selector: 'app-new-year-2018-game',
	templateUrl: './new-year-2018-game.component.html',
	styleUrls: ['./new-year-2018-game.component.css']
})
export class NewYear2018GameComponent implements OnInit {
	scoreboards: any[] = [];
	topItems: any[] = [];
	scoreboardsPage: number = 1;
	topPage: number = 1;

	constructor(private api: ApiService) { }

	ngOnInit() {
		this.loadMoreScoreboards();
		this.loadMoreTop();
	}

	loadMoreScoreboards() {
        this.api.get(ApiConfig.NEW_YEAR_2018_GAME_SCOREBOARD_URL, {page: this.scoreboardsPage})
        .subscribe(result => {
            for (var scoreboard of result.results) {
                this.scoreboards.push(scoreboard);
            }

            if (!result.next) {
                this.loadMoreScoreboards = () => {};
            	return;
            }

            ++this.scoreboardsPage;

            if (scoreboardsContainer.scrollWidth < newYear2018GameComponent.scrollWidth + 500)
                setTimeout(() => this.loadMoreScoreboards(), 100);
        });
    }

    loadMoreTop() {
        this.api.get(ApiConfig.NEW_YEAR_2018_GAME_TOP_URL, {page: this.topPage}).subscribe(result => {
            for (var topItem of result.results) {
                this.topItems.push(topItem);
            }

            if (!result.next) {
                this.loadMoreTop = () => {};
            	return;
            }

            ++this.topPage;

            if (newYear2018GameComponent.scrollHeight <= newYear2018GameComponent.clientHeight)
            	setTimeout(() => this.loadMoreTop(), 100);
        });
    }

    onScrollScoreboards() {
    	this.loadMoreScoreboards();
    }
    onScrollTop() {
    	this.loadMoreTop();
    }
}
