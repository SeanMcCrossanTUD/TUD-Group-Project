import { Routes } from '@angular/router';
import { UserRegisterComponent } from './user-register/user-register.component';
import { LandingPageComponent } from './landing-page/landing-page.component';

export const routes: Routes = [
    
    { path: 'user-register', component:UserRegisterComponent  },
    {path:'', component:LandingPageComponent}
];
