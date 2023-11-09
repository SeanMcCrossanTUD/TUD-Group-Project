import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MissingValuesChartComponent } from './missing-values-chart.component';

describe('MissingValuesChartComponent', () => {
  let component: MissingValuesChartComponent;
  let fixture: ComponentFixture<MissingValuesChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MissingValuesChartComponent]
    });
    fixture = TestBed.createComponent(MissingValuesChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
