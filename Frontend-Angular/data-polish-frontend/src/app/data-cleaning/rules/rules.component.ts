import { Component, ViewChild } from '@angular/core';
import { DataPreviewDataService } from 'src/app/Services/Datacleaning/data-preview-data.service';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent } from 'ag-grid-community';

import 'ag-grid-enterprise';
@Component({
  selector: 'app-rules',
  templateUrl: './rules.component.html',
  styleUrls: ['./rules.component.css']
})
export class RulesComponent {



  constructor(
    private DataPreviewDataService:DataPreviewDataService,
 
    ){

  }
  DatapreviewColumnNames=[{field:"naveen"},{field:"naveen"}]
  DatapreviewData=[{"naveen":123},{'naveen':'abc'}];

  ngOnInit(){
    // this.DataPreviewDataService.getData().subscribe(
    //   (response:any)=>{
    //     this.DatapreviewColumnNames=response.coloumnNames;
    //     this.DatapreviewData=response.data;
    //     this.makeHeaser();
    //     this.rowData=this.DatapreviewData;
    //   }
    // )

 
    
   
  
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

  public sideBar:any= ['columns'];
  rowData=this.DatapreviewData;
  columnDefs=this.DatapreviewColumnNames;
  public defaultColDef: ColDef = {
    initialWidth: 150,
    sortable: true,
    resizable: true,
    filter: true,
    //enableValue: true,
    // allow every column to be grouped
    // enableRowGroup: true,
    // // allow every column to be pivoted
    // enablePivot: true,
   };

   
}
  


