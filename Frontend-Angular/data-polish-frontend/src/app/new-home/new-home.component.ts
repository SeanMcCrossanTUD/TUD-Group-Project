import { Component } from '@angular/core';
import { NavigatationService } from '../Services/navigate/navigatation.service'; 

@Component({
  selector: 'app-new-home',
  templateUrl: './new-home.component.html',
  styleUrls: ['./new-home.component.css']
})
export class NewHomeComponent {
  constructor(
    private NavigatationService:NavigatationService
  ){}

  navigate(e:any){
    this.NavigatationService.navigate(e);
  }
}
