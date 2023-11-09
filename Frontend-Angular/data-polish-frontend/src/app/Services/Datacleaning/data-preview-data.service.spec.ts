import { TestBed } from '@angular/core/testing';

import { DataPreviewDataService } from './data-preview-data.service';

describe('DataPreviewDataService', () => {
  let service: DataPreviewDataService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DataPreviewDataService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
