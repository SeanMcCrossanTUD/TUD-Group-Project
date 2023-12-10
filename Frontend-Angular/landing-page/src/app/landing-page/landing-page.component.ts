import { Component } from '@angular/core';

@Component({
  selector: 'app-landing-page',
  standalone: true,
  imports: [],
  templateUrl: './landing-page.component.html',
  styleUrl: './landing-page.component.css'
})
export class LandingPageComponent {
  openTutorial() {
    console.log('Opening tutorial...');
    // Add logic to navigate to the tutorial page or show a modal
  }

  getStarted() {
    console.log('Getting started...');
    // Add logic to navigate to the get started page or perform other actions
  }
}
