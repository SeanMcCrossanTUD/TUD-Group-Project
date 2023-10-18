import { Component } from '@angular/core';
import { Router } from '@angular/router';
@Component({
  selector: 'app-data-cleaning',
  templateUrl: './data-cleaning.component.html',
  styleUrls: ['./data-cleaning.component.css']
})
export class DataCleaningComponent {
  constructor(private router: Router){

  }
  StartCleaning(){
    alert("data cleaning is started...");
    this.router.navigate(["/Export"]);

  }
}
