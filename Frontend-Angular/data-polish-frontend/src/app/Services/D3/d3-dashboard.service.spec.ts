import { TestBed } from '@angular/core/testing';

import { D3DashboardService } from './d3-dashboard.service';

describe('D3DashboardService', () => {
  let service: D3DashboardService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(D3DashboardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
