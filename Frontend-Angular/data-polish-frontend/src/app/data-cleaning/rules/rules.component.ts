import { Component, ViewChild } from '@angular/core';
import { DataPreviewDataService } from 'src/app/Services/Datacleaning/data-preview-data.service';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent } from 'ag-grid-community';
import { AdvanceOptionsButtonComponent } from './nested-components/advance-options-button/advance-options-button.component';

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
  visible=false;
  DatapreviewColumnNames= [
    {field:"Field Names"},
    // {field:"Data Type"},
    {field:"Keep column",editable: true},
    {field:"Advanced options",cellRenderer: AdvanceOptionsButtonComponent,
    cellRendererParams: {
      clicked: (x:any)=>{
        this.visible=true;
    }
  }
    },
  ]

  dummy(e:any){
    alert(e);
  }
  DatapreviewData=[{"Field Names":123,"Data Type":"boolean",
  "Keep column":true,
  "Advanced options":"abc"

},{'naveen':'abc'}];

  ngOnInit(){
    this.DataPreviewDataService.getJsonData2().subscribe(
      (response:any)=>{
       
        this.makedata(response.columnNames);
       
      }
    )

 
    
   
  
  }

  makedata(columnNames:any){
    var temp:any=[];
    columnNames.forEach((item:any)=>{
      temp.push(
        {
          "Field Names":item,
          "Keep column":true,
          "Advanced options":item
        }
      )
    })
    this.rowData=temp;

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
  rowData:any=[]
  columnDefs=[];
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
  


