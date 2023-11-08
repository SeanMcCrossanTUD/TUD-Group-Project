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
import { MissingValuesChartComponent } from './D3/missing-values-chart/missing-values-chart.component';
import { DataTypesChartComponent } from './D3/data-types-chart/data-types-chart.component';

const routes: Routes = [
    {path:'',component:HomePageComponent},
    {path:'UploadDataset',component:UploadFileComponent},
    {path:'DataProfile',component:DataProfileComponent},
    {path:'Export',component:ExportComponent},
    {path:'DataCleaning',component:DataCleaningComponent}

];
@NgModule({
  declarations: [
    AppComponent,
    UploadFileComponent,
    DataProfileComponent,
    HomePageComponent,
    ExportComponent,
    DataCleaningComponent,
    MissingValuesChartComponent,
    DataTypesChartComponent
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
    FormsModule
    
    
  ],
  providers: [
    MessageService,
    CookieService,
    TerminalService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
