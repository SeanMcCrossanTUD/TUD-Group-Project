import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { AppComponent } from './app.component';
import { Routes,RouterModule } from '@angular/router';
import { LandingPageComponent } from './landing-page/landing-page.component';
import { HttpClientModule } from '@angular/common/http';
import {StyleClassModule} from 'primeng/styleclass';
import { ButtonModule } from 'primeng/button';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { InputNumberModule } from 'primeng/inputnumber';
import { UserRegistarationComponent } from './user-registaration/user-registaration.component';
import { FormsModule } from '@angular/forms';
import { ToastModule } from 'primeng/toast';
import {MessageService} from 'primeng/api';
import { SetPasswordComponent } from './set-password/set-password.component';
import { ForgetPasswordComponent } from './forget-password/forget-password.component';
// import { HomeComponent } from './home/home.component';
const routes: Routes = [
    
    {path:'user-registration',component:UserRegistarationComponent},
    {path:'set-password',component:SetPasswordComponent},
    {path:'forget-password',component:ForgetPasswordComponent},
    {path:'',component:LandingPageComponent}


];
@NgModule({
  declarations: [
    AppComponent,
    LandingPageComponent,
    UserRegistarationComponent,
    SetPasswordComponent,
    ForgetPasswordComponent
    // HomeComponent
  ],
  imports: [
    StyleClassModule,
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    BrowserModule,
    ButtonModule,
    InputNumberModule,
    ToastModule,
    FormsModule,
    RouterModule.forRoot(routes,{useHash: true}),
  ],
  providers: [MessageService],
  bootstrap: [AppComponent]
})
export class AppModule { }