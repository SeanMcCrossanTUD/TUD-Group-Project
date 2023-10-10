import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UploadFileComponent } from './upload-file/upload-file.component';
import { Routes, RouterModule } from '@angular/router';
import { DataProfileComponent } from './data-profile/data-profile.component';
import { HomePageComponent } from './home-page/home-page.component'; // CLI imports router
const routes: Routes = [
    {path:'',component:HomePageComponent},
    {path:'UploadDataset',component:UploadFileComponent},
    {path:'DataProfile',component:DataProfileComponent}
];
@NgModule({
  declarations: [
    AppComponent,
    UploadFileComponent,
    DataProfileComponent,
    HomePageComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
