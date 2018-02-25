import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SecretPageForLactariusComponent } from './secret-page-for-lactarius.component';

describe('SecretPageForLactariusComponent', () => {
  let component: SecretPageForLactariusComponent;
  let fixture: ComponentFixture<SecretPageForLactariusComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SecretPageForLactariusComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SecretPageForLactariusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
