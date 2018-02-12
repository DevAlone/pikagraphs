import { Component, OnInit, Input, ViewChild, ElementRef  } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { User } from '../user';
import { UserService } from '../user.service';
import {LoadingAnimationService} from '../loading-animation.service';


const l4reverSignupTimestamp = 1274536587;


@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrls: ['./user.component.css']
})
export class UserComponent implements OnInit {
    @Input() user: User;
    @ViewChild('l4reverEasterEggValue')
    l4reverEasterEggValue: ElementRef;

    constructor(
        private loadingAnimationService: LoadingAnimationService,
        private route: ActivatedRoute,
        private userService: UserService,
        private location: Location,
    ) {}

    ngOnInit() {
        this.loadingAnimationService.start();
        this.route.params.subscribe(params => {
            this.userService.getUserByName(params.username)
                .subscribe(response => {
                    this.loadingAnimationService.stop();
                    this.user = response.data;
                });

            this._l4rverEasterEggTimer();
        });
    }

    _l4rverEasterEggTimer() {
        if (this.l4reverEasterEggValue) {
            this.l4reverEasterEggValue.nativeElement.textContent = parseInt(
              (Date.now() / 1000 - l4reverSignupTimestamp).toString(), 10
            );
        }

        setTimeout(() => this._l4rverEasterEggTimer(), 1000);
    }
}
