import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';

@Component({
  selector: 'app-home-page',
  templateUrl: './home-page.component.html',
  styleUrls: ['./home-page.component.css']
})
export class HomePageComponent {
  constructor(private messageService:MessageService){

  }
  copytoclipboard(e:any){
    navigator.clipboard.writeText(e);
    this.messageService.add({ severity: 'success', summary: 'ID copied ' });

  }
}
