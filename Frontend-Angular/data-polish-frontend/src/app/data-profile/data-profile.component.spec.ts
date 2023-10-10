import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataProfileComponent } from './data-profile.component';

describe('DataProfileComponent', () => {
  let component: DataProfileComponent;
  let fixture: ComponentFixture<DataProfileComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DataProfileComponent]
    });
    fixture = TestBed.createComponent(DataProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
