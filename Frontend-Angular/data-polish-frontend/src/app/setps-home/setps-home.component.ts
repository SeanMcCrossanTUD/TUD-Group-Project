import { Component } from '@angular/core';
import { MenuItem, MessageService } from 'primeng/api';

@Component({
  selector: 'app-setps-home',
  templateUrl: './setps-home.component.html',
  styleUrls: ['./setps-home.component.css']
})
export class SetpsHomeComponent {
 
  activeIndex: number = 0;

  movenext(){
    this.activeIndex++;
  }
  moveBack(){
    this.activeIndex--;
  }

}
