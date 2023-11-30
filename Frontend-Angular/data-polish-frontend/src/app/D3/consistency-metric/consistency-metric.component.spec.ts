import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConsistencyMetricComponent } from './consistency-metric.component';

describe('ConsistencyMetricComponent', () => {
  let component: ConsistencyMetricComponent;
  let fixture: ComponentFixture<ConsistencyMetricComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ConsistencyMetricComponent]
    });
    fixture = TestBed.createComponent(ConsistencyMetricComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
