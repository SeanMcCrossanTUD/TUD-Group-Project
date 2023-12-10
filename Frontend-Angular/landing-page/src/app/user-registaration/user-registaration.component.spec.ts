import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UserRegistarationComponent } from './user-registaration.component';

describe('UserRegistarationComponent', () => {
  let component: UserRegistarationComponent;
  let fixture: ComponentFixture<UserRegistarationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UserRegistarationComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(UserRegistarationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
