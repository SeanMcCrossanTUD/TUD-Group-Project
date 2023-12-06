import { TestBed } from '@angular/core/testing';

import { DataCleaningService } from './data-cleaning.service';

describe('DataCleaningService', () => {
  let service: DataCleaningService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DataCleaningService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
