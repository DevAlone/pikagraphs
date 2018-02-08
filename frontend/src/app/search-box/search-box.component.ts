import { Component, OnInit, Input } from '@angular/core';
import { Subject } from 'rxjs/Subject';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { ActivatedRoute, Router, Params } from '@angular/router';


@Component({
  selector: 'app-search-box',
  host: {'(window:keydown)': 'keyEvent($event)'},
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.css']
})
export class SearchBoxComponent implements OnInit {
	@Input()
	callback: string;
	@Input()
	parent: any;
	@Input()
	sortByFields: any[];

	private searchTerms = new Subject<string>();

	public searchText: string = "";
	public sortBy: string = "";
    public reverseSort: boolean = false;

    keyEvent(event) {
        if (event.keyCode == 82)
            this.update();
    }

	constructor(
        private route: ActivatedRoute,
        private router: Router
    ) {
        this.route.queryParams.subscribe(params => {
            if (params['search_text'])
                this.searchText = params['search_text'];
            if (params['sort_by'])
                this.sortBy = params['sort_by'];
            if (params['reverse_sort'])
                this.reverseSort = params['reverse_sort'] == "true";    
        
        });
    }

    public get currentSortByField(): any {
        var ordering: string = this.sortBy;
        if (ordering.startsWith('-'))
            ordering = ordering.substr(1);

        if (ordering)
            return this.sortByFields.find(value => value.fieldName == ordering);
        else
            return this.sortByFields[0];
    }


	ngOnInit() {
        if (!this.route.snapshot.queryParams['search_text'] 
                && !this.route.snapshot.queryParams['sort_by'] 
                && !this.route.snapshot.queryParams['reverse_sort']) {
            this.sortBy = this.sortByFields[0].fieldName;
            this.reverseSort = true;
            this.updateUrl();
        }


		this.searchTerms.pipe(
            // wait 300ms after each keystroke before considering the term
            debounceTime(300),
            // ignore new term if same as previous term
            distinctUntilChanged(),
        ).subscribe(term => {
        	this.searchText = term;
        	this.update();
        });

        this.update();
	}

	search(term: string): void {
        this.searchTerms.next(term);
    }

    sortByClicked(field: any) {
        var sortBy = field.fieldName;

        if (this.sortBy == sortBy)
            this.reverseSort = !this.reverseSort;
        else
            this.sortBy = sortBy;

        this.update();
    }

    update(): void {
        this.updateUrl();
    	this.parent[this.callback]({
    		search_text: this.searchText,
    		order_by: (this.reverseSort ? '-': '') + this.sortBy,
    	});
    }

    updateUrl() {
        const queryParams: Params = Object.assign({}, this.route.snapshot.queryParams);

        queryParams['search_text'] = this.searchText;
        queryParams['sort_by'] = this.sortBy;
        queryParams['reverse_sort'] = this.reverseSort ? 'true': 'false';

        this.router.navigate([], { queryParams: queryParams, replaceUrl: true });
    }

    getFieldHumanReadableName(field: any): string {
        if (typeof field.humanReadableName === 'string')
            return field.humanReadableName;
        else
            return field.humanReadableName.sortBy
    }
}
