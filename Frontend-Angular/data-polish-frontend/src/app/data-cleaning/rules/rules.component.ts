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
  currentrow=''
  DatapreviewColumnNames= [
    {field:"Field Names",
    width: 200
  },
    // {field:"Data Type"},
    {
      field:"Keep column",
    editable: true,
    width: 200
  }
    ,
    {
      field:"Advanced cleaning options",
      cellRenderer: AdvanceOptionsButtonComponent,
      cellRendererParams: {
      clicked: (x:any)=>{
        this.currentrow=x;      
        this.visible=true;
          }
     },
     width:300

    },
  ]


  DatapreviewData=[{"Field Names":123,"Data Type":"boolean",
  "Keep column":true,
  "Advanced cleaning options":"abc"

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
          "Advanced cleaning options":item
        }
      )
    })
    this.rowData=temp;

  }

  
  inlineEdit(e:any){
   console.log(this.rowData);
  }
  public sideBar:any= ['columns'];
  rowData:any=[]
 
  public defaultColDef: ColDef = {
    initialWidth: 150,
    sortable: true,
    resizable: true,
    filter: true,
    //onCellValueChanged: (event) => this.inlineEdit(event),
    //enableValue: true,
    // allow every column to be grouped
    // enableRowGroup: true,
    // // allow every column to be pivoted
    // enablePivot: true,
   };

   rules:any={
    "columns_kept":[],
    "trim_whitespace":[],
    "remove_special_characters":[]
   }

   setdata(){
    var temp:any=[];
      this.rowData.forEach((x:any)=>{
        if(x["Keep column"]==true){
          temp.push(x["Field Names"]);
        }
      })

      this.rules.columns_kept=temp;
      console.log(this.rules);
   }

   
   ////// cbs

   cb_remove_special_characters=false
   cb_trim_whitespace=false

   setallCBTOFalse(){
    this.cb_remove_special_characters=false;
    this.cb_trim_whitespace=false;
   }
   savechangestorules(){
  
   if(this.cb_remove_special_characters){
    this.setRemoveSpecialCharacters(this.currentrow);
   }
   if(this.cb_trim_whitespace){
    this.setTrimWhiteSpaces(this.currentrow);
   }
   this.visible=false;
   this.currentrow='';
   this.setallCBTOFalse();
   }

   setTrimWhiteSpaces(x:any){
    this.rules["trim_whitespace"].push(x);
    console.log(this.rules)
   }
   setRemoveSpecialCharacters(x:any){
    this.rules["remove_special_characters"].push(x);
    console.log(this.rules)
   }
}
  


