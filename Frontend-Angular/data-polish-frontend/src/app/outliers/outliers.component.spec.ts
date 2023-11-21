import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OutliersComponent } from './outliers.component';

describe('OutliersComponent', () => {
  let component: OutliersComponent;
  let fixture: ComponentFixture<OutliersComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [OutliersComponent]
    });
    fixture = TestBed.createComponent(OutliersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
