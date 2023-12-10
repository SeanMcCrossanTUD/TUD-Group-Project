import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Routes,RouterModule } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { UserRegisterComponent } from './user-register/user-register.component';
// import { HomeComponent } from './home/home.component';
const routes: Routes = [
    {path:'',component:LandingPageComponent},
    {path:'user-registration',component:UserRegisterComponent}


];
@NgModule({
  declarations: [
    AppComponent,
    // HomeComponent
  ],
  imports: [
    BrowserModule,
    RouterModule.forRoot(routes,{useHash: true}),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }