import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardinalityComponent } from './cardinality.component';

describe('CardinalityComponent', () => {
  let component: CardinalityComponent;
  let fixture: ComponentFixture<CardinalityComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CardinalityComponent]
    });
    fixture = TestBed.createComponent(CardinalityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});