import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdvanceOptionsButtonComponent } from './advance-options-button.component';

describe('AdvanceOptionsButtonComponent', () => {
  let component: AdvanceOptionsButtonComponent;
  let fixture: ComponentFixture<AdvanceOptionsButtonComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AdvanceOptionsButtonComponent]
    });
    fixture = TestBed.createComponent(AdvanceOptionsButtonComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
