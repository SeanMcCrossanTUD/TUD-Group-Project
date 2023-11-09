import { TestBed } from '@angular/core/testing';

import { NavigatationService } from './navigatation.service';

describe('NavigatationService', () => {
  let service: NavigatationService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(NavigatationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
