import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { UploadFileComponent } from './upload-file/upload-file.component';
import { Routes, RouterModule } from '@angular/router';
import { DataProfileComponent } from './data-profile/data-profile.component';
import { HomePageComponent } from './home-page/home-page.component';
import { ExportComponent } from './export/export.component'; // CLI imports router
import { ButtonModule } from 'primeng/button';
import { DialogModule } from 'primeng/dialog';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FileUploadModule } from 'primeng/fileupload';
import { ToastModule } from 'primeng/toast';
import {MessageService} from 'primeng/api';
import { DataCleaningComponent } from './data-cleaning/data-cleaning.component'
import { ConfirmDialogModule } from 'primeng/confirmdialog';
import { ContextMenuModule } from 'primeng/contextmenu';
import { SidebarModule } from 'primeng/sidebar';
import {CookieService} from 'ngx-cookie-service';
import { TerminalModule, TerminalService } from 'primeng/terminal';
import { DockModule } from 'primeng/dock';
import { FormsModule } from '@angular/forms';
import { AppSettings } from './Const/config';
import { NewHomeComponent } from './new-home/new-home.component';
import { SetpsHomeComponent } from './setps-home/setps-home.component';
import { NavigatationService } from './Services/navigate/navigatation.service';
import { TabViewModule } from 'primeng/tabview';
import { StepsModule } from 'primeng/steps';
import { SpeedDialModule } from 'primeng/speeddial';
import { DataPreviewComponent } from './data-preview/data-preview.component';
import { SplitterModule } from 'primeng/splitter';
const routes: Routes = [
    {path:'',component:UploadFileComponent},
    {path:'newjob',component:SetpsHomeComponent},
    {path:'1',component:UploadFileComponent},
    {path:'2',component:DataPreviewComponent},
    {path:'3',component:DataProfileComponent},
    {path:'4',component:DataCleaningComponent},
    {path:'5',component:ExportComponent},

];
@NgModule({
  declarations: [
    AppComponent,
    UploadFileComponent,
    DataProfileComponent,
    HomePageComponent,
    ExportComponent,
    DataCleaningComponent,
    NewHomeComponent,
    SetpsHomeComponent,
    DataPreviewComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ButtonModule,
    DialogModule,
    BrowserAnimationsModule,
    FileUploadModule,
    ToastModule,
    ConfirmDialogModule,
    ContextMenuModule,
    SidebarModule,
    TerminalModule,
    DockModule,
    FormsModule,
    TabViewModule,
    StepsModule,
    SpeedDialModule,
    SplitterModule
    
    
  ],
  providers: [
    MessageService,
    CookieService,
    TerminalService,
    NavigatationService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
