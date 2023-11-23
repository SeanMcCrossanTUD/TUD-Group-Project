import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataQualityMetricComponent } from './data-quality-metric.component';

describe('DataQualityMetricComponent', () => {
  let component: DataQualityMetricComponent;
  let fixture: ComponentFixture<DataQualityMetricComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DataQualityMetricComponent]
    });
    fixture = TestBed.createComponent(DataQualityMetricComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
