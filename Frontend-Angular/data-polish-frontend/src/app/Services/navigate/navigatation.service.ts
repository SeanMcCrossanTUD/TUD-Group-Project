import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
@Injectable({
  providedIn: 'root',
})
export class NavigatationService {
  constructor(private router: Router) {}

  public navigate(e: any) {
    this.router.navigate([e]);
  }
}
