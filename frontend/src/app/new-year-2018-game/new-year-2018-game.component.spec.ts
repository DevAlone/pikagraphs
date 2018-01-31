import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { NewYear2018GameComponent } from './new-year-2018-game.component';

describe('NewYear2018GameComponent', () => {
  let component: NewYear2018GameComponent;
  let fixture: ComponentFixture<NewYear2018GameComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ NewYear2018GameComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(NewYear2018GameComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
