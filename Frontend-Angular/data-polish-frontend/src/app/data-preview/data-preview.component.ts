import { Component, Input, ViewChild } from '@angular/core';
import { DataPreviewDataService } from '../Services/Datacleaning/data-preview-data.service';
import { fadeInAnimation } from '../Animations/animation';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent } from 'ag-grid-community';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import 'ag-grid-enterprise';
import { MessageService } from 'primeng/api';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-data-preview',
  templateUrl: './data-preview.component.html',
  styleUrls: ['./data-preview.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class DataPreviewComponent {
  height = '50vh';
  gridStyle="width: 80vw;height:"+this.height
  
  constructor(
    private DataPreviewDataService:DataPreviewDataService,
    private http: HttpClient,
    private CookieService:CookieService,
    private MessageService:MessageService
    ){

  }
  DatapreviewColumnNames=[]
  DatapreviewData=[];

  getblob(x:any){
    alert('hi')
   
  }
  dataloaded=false;
  hidepregress=false;

  ngOnInit(){
    var url=String(window.location);
    var pageNumber=url.charAt(url.length-1)
    if(pageNumber=='2'){
      this.height='80vh'
      this.gridStyle="width: 80vw;height:"+this.height
    }
    var id=this.CookieService.get('jobsid');
    this.DataPreviewDataService.getData(id).subscribe(
      (Response)=>{
     
        this.DataPreviewDataService.getJsonData(Response).subscribe(
          (r2:any)=>{
           
            this.DatapreviewColumnNames=r2.columnNames;

            this.rowData=r2.data
            this.makeHeaser();
           this.dataloaded=true
         

            
          }
        )
      },
      (Error)=>{
        this.hidepregress=true;
        this.MessageService.add({ severity: 'error', summary: 'Try again ', detail: "your file is still processing..." });
     
      }
    )


    

 
    
   
  
  }

  refresh(){
    var id=this.CookieService.get('jobsid');
    this.DataPreviewDataService.getData(id).subscribe(
      (Response)=>{
     
        this.DataPreviewDataService.getJsonData(Response).subscribe(
          (r2:any)=>{
          
            this.DatapreviewColumnNames=r2.columnNames;
   
            this.rowData=r2.data
            this.makeHeaser();
            this.dataloaded=true
          }
        )
      },
      (Error)=>{
        this.MessageService.add({ severity: 'error', summary: 'Error', detail: "your file is still processing..." });
     
      }
    )
  }

  makeHeaser(){
    var temp: any=[];
   // var i=0;
   this.DatapreviewColumnNames.forEach((element)=>{
    // if(i<1){
    //   temp.push({field:element,header:element,rowDrag: true})
    //   i++
      
    // }else{
      temp.push({field:element,header:element})
    //}

   })
   this.columnDefs=temp;
  
  }

  public sideBar:any= ['columns','filters'];
  rowData=[]
  columnDefs=[]
  public defaultColDef: ColDef = {
    initialWidth: 150,
    sortable: true,
    resizable: true,
    filter: true,
    enableValue: true,
    // allow every column to be grouped
    enableRowGroup: true,
    // allow every column to be pivoted
    enablePivot: true,
   };

   
}
  


