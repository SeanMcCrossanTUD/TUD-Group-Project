import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DuplicateChartComponent } from './duplicate-chart.component';

describe('DuplicateChartComponent', () => {
  let component: DuplicateChartComponent;
  let fixture: ComponentFixture<DuplicateChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DuplicateChartComponent]
    });
    fixture = TestBed.createComponent(DuplicateChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
