import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CorrelationScatterPlotComponent } from './correlation-scatter-plot.component';

describe('CorrelationScatterPlotComponent', () => {
  let component: CorrelationScatterPlotComponent;
  let fixture: ComponentFixture<CorrelationScatterPlotComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CorrelationScatterPlotComponent]
    });
    fixture = TestBed.createComponent(CorrelationScatterPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
