import { Component, ViewChild } from '@angular/core';
import { DataPreviewDataService } from '../Services/Datacleaning/data-preview-data.service';
import { fadeInAnimation } from '../Animations/animation';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent } from 'ag-grid-community';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import 'ag-grid-enterprise';

@Component({
  selector: 'app-data-preview',
  templateUrl: './data-preview.component.html',
  styleUrls: ['./data-preview.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class DataPreviewComponent {

  constructor(
    private DataPreviewDataService:DataPreviewDataService,
    private http: HttpClient
    ){

  }
  DatapreviewColumnNames=[]
  DatapreviewData=[];

  ngOnInit(){
    this.DataPreviewDataService.getData().subscribe(
      (response:any)=>{
        this.DatapreviewColumnNames=response.columnNames;
        this.DatapreviewData=response.data;
       
        this.makeHeaser();
        this.rowData=this.DatapreviewData;
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
  

