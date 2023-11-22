import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OutliersScatterPlotComponent } from './outliers-scatter-plot.component';

describe('OutliersScatterPlotComponent', () => {
  let component: OutliersScatterPlotComponent;
  let fixture: ComponentFixture<OutliersScatterPlotComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OutliersScatterPlotComponent]
    });
    fixture = TestBed.createComponent(OutliersScatterPlotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
