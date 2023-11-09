import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DataPreviewComponent } from './data-preview.component';

describe('DataPreviewComponent', () => {
  let component: DataPreviewComponent;
  let fixture: ComponentFixture<DataPreviewComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DataPreviewComponent]
    });
    fixture = TestBed.createComponent(DataPreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
