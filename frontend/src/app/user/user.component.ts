import { Component, OnInit, Input, ViewChild, ElementRef  } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Location } from '@angular/common';
import { User } from '../user';
import { UserService } from '../user.service';

var l4reverSignupTimestamp: number = 1274536587;


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
        private route: ActivatedRoute,
        private userService: UserService,
        private location: Location
    ) {}

    ngOnInit() {
        this.route.params.subscribe(params => {
            this.userService.getUserByName(params.username)
                .subscribe(user => this.user = user);

            this._l4rverEasterEggTimer();
        })
    }

    _l4rverEasterEggTimer() {        
        if (this.l4reverEasterEggValue)
            this.l4reverEasterEggValue.nativeElement.textContent = parseInt(
                (Date.now() / 1000 - l4reverSignupTimestamp).toString()
            );

        setTimeout(() => this._l4rverEasterEggTimer(), 1000);
    }
}
