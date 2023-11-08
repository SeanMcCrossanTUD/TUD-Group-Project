import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataTypesChartComponent } from './data-types-chart.component';

describe('DataTypesChartComponent', () => {
  let component: DataTypesChartComponent;
  let fixture: ComponentFixture<DataTypesChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DataTypesChartComponent]
    });
    fixture = TestBed.createComponent(DataTypesChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
