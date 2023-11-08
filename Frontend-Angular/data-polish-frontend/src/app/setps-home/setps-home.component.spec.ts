import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SetpsHomeComponent } from './setps-home.component';

describe('SetpsHomeComponent', () => {
  let component: SetpsHomeComponent;
  let fixture: ComponentFixture<SetpsHomeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SetpsHomeComponent]
    });
    fixture = TestBed.createComponent(SetpsHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
