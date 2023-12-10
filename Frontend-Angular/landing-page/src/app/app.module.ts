import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Routes,RouterModule } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';

import {StyleClassModule} from 'primeng/styleclass';
import { ButtonModule } from 'primeng/button';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { InputNumberModule } from 'primeng/inputnumber';
import { UserRegistarationComponent } from './user-registaration/user-registaration.component';

// import { HomeComponent } from './home/home.component';
const routes: Routes = [
    {path:'',component:LandingPageComponent},
    {path:'user-registration',component:UserRegistarationComponent}


];
@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    UserRegistarationComponent
    // HomeComponent
  ],
  imports: [
    StyleClassModule,
    BrowserModule,
    BrowserAnimationsModule,
    BrowserModule,
    ButtonModule,
    InputNumberModule,
    RouterModule.forRoot(routes,{useHash: true}),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }