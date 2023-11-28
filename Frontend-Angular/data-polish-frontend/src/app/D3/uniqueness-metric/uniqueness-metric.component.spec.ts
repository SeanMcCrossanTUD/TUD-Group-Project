import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UniquenessMetricComponent } from './uniqueness-metric.component';

describe('UniquenessMetricComponent', () => {
  let component: UniquenessMetricComponent;
  let fixture: ComponentFixture<UniquenessMetricComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UniquenessMetricComponent]
    });
    fixture = TestBed.createComponent(UniquenessMetricComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
