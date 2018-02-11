import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LoadingAnimationComponent } from './loading-animation.component';

describe('LoadingAnimationComponent', () => {
  let component: LoadingAnimationComponent;
  let fixture: ComponentFixture<LoadingAnimationComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LoadingAnimationComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LoadingAnimationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
