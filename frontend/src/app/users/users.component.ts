import { Component, OnInit } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { Subject } from 'rxjs/Subject';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';

import { UserService } from '../user.service';
import { User } from '../user';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
    users$: Observable<any>;
    users: User[];
    private searchTerms = new Subject<string>();

    constructor(private userService: UserService) { }

    search(term: string): void {
        console.log('UsersComponent: ' + term);
        this.searchTerms.next(term);
    }

    ngOnInit(): void {
        this.users$ = this.searchTerms.pipe(
            // wait 300ms after each keystroke before considering the term
            debounceTime(300),
            // ignore new term if same as previous term
            distinctUntilChanged(),
            // switch to new search observable each time the term changes
            switchMap((term: string) => this.userService.searchUsers(term)),
        );
        this.users$.subscribe(result => {
            if (!result.count)
                return;

            this.users = result.results;  // this.users.concat(result.results);
        })
    }
}
