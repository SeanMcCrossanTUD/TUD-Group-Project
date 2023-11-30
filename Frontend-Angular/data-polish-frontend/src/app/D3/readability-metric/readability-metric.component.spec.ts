import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReadabilityMetricComponent } from './readability-metric.component';

describe('ReadabilityMetricComponent', () => {
  let component: ReadabilityMetricComponent;
  let fixture: ComponentFixture<ReadabilityMetricComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ReadabilityMetricComponent]
    });
    fixture = TestBed.createComponent(ReadabilityMetricComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
