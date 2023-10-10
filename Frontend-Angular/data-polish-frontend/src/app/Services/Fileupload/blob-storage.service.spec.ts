import { TestBed } from '@angular/core/testing';

import { BlobStorageService } from './blob-storage.service';

describe('BlobStorageService', () => {
  let service: BlobStorageService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BlobStorageService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
