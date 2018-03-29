import {
  Component, OnInit, Input, ViewChild, ViewChildren, QueryList, ElementRef
} from '@angular/core';

@Component({
  selector: 'app-nice-link',
  templateUrl: './nice-link.component.html',
  styleUrls: ['./nice-link.component.css']
})
export class NiceLinkComponent implements OnInit {
  @Input() href: string;
  @Input() title: string;

  constructor() { }

  ngOnInit() {
  }
}
