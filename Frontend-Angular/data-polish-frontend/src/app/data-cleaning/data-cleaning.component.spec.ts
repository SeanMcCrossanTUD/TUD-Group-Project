import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataCleaningComponent } from './data-cleaning.component';

describe('DataCleaningComponent', () => {
  let component: DataCleaningComponent;
  let fixture: ComponentFixture<DataCleaningComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DataCleaningComponent]
    });
    fixture = TestBed.createComponent(DataCleaningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
