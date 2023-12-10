import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  standalone: true 
})
export class AppComponent {
  openTutorial() {
    console.log('Opening tutorial...');
    // Add logic to navigate to the tutorial page or show a modal
  }

  getStarted() {
    console.log('Getting started...');
    // Add logic to navigate to the get started page or perform other actions
  }
}
