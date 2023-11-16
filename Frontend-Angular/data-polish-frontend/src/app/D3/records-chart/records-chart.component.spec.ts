import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RecordsChartComponent } from './records-chart.component';

describe('RecordsChartComponent', () => {
  let component: RecordsChartComponent;
  let fixture: ComponentFixture<RecordsChartComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [RecordsChartComponent]
    });
    fixture = TestBed.createComponent(RecordsChartComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
