import { TestBed, inject } from '@angular/core/testing';

import { CommunityService } from './community.service';

describe('CommunityService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CommunityService]
    });
  });

  it('should be created', inject([CommunityService], (service: CommunityService) => {
    expect(service).toBeTruthy();
  }));
});
