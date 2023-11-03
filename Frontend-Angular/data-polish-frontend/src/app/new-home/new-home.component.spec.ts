import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewHomeComponent } from './new-home.component';

describe('NewHomeComponent', () => {
  let component: NewHomeComponent;
  let fixture: ComponentFixture<NewHomeComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NewHomeComponent]
    });
    fixture = TestBed.createComponent(NewHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
