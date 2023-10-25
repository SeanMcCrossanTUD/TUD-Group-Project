import { TestBed } from '@angular/core/testing';

import { AccessibilityServiceService } from './accessibility-service.service';

describe('AccessibilityServiceService', () => {
  let service: AccessibilityServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(AccessibilityServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
