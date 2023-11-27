import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BubbleChartComponent } from './bubble-chart.component';

describe('BubbleChartComponent', () => {
  let component: BubbleChartComponent;
  let fixture: ComponentFixture<BubbleChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [BubbleChartComponent]
    });
    fixture = TestBed.createComponent(BubbleChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
