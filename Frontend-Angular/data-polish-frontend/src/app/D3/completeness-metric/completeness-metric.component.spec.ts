import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CompletenessMetricComponent } from './completeness-metric.component';

describe('CompletenessMetricComponent', () => {
  let component: CompletenessMetricComponent;
  let fixture: ComponentFixture<CompletenessMetricComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CompletenessMetricComponent]
    });
    fixture = TestBed.createComponent(CompletenessMetricComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
