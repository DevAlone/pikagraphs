import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NiceLinkComponent } from './nice-link.component';

describe('NiceLinkComponent', () => {
  let component: NiceLinkComponent;
  let fixture: ComponentFixture<NiceLinkComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NiceLinkComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NiceLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
