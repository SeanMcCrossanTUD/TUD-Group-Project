import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NumberFieldsChartComponent } from './number-fields-chart.component';

describe('NumberFieldsChartComponent', () => {
  let component: NumberFieldsChartComponent;
  let fixture: ComponentFixture<NumberFieldsChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NumberFieldsChartComponent]
    });
    fixture = TestBed.createComponent(NumberFieldsChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
