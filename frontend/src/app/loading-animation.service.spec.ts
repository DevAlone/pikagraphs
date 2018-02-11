import { TestBed, inject } from '@angular/core/testing';

import { LoadingAnimationService } from './loading-animation.service';

describe('LoadingAnimationService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [LoadingAnimationService]
    });
  });

  it('should be created', inject([LoadingAnimationService], (service: LoadingAnimationService) => {
    expect(service).toBeTruthy();
  }));
});
