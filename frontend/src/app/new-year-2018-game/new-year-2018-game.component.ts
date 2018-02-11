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
    scoreboardsPage = 0;
    topPage = 0;

    constructor(private api: ApiService) { }
    ngOnInit() {
      this.loadMoreScoreboards();
      this.loadMoreTop();
    }

    loadMoreScoreboards() {
        this.api.get(ApiConfig.NEW_YEAR_2018_GAME_SCOREBOARD_URL, {page: this.scoreboardsPage})
        .subscribe(result => {
            for (const scoreboard of result.data) {
                this.scoreboards.push(scoreboard);
            }

            if (!result.data.length) {
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
            for (const topItem of result.data) {
                this.topItems.push(topItem);
            }

            if (!result.data.length) {
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
