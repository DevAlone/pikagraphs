import { Component, OnInit, Input } from '@angular/core';
import { CommunityService } from '../community.service';
import { ActivatedRoute } from '@angular/router';
import { Community } from '../community';


@Component({
    selector: 'app-community',
    templateUrl: './community.component.html',
    styleUrls: ['./community.component.css']
})
export class CommunityComponent implements OnInit {
    @Input() community: Community;

    constructor(
        private route: ActivatedRoute,
        private communityService: CommunityService
    ) { }

    ngOnInit() {
        this.route.params.subscribe(params => {
            this.communityService.getCommunityByUrlName(params.url_name)
                .subscribe(response => this.community = response.data);
        });
    }
}
