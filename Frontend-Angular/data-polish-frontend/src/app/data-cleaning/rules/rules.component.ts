import { Component, ViewChild } from '@angular/core';
import { DataPreviewDataService } from 'src/app/Services/Datacleaning/data-preview-data.service';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent,GridApi } from 'ag-grid-community';
import { AdvanceOptionsButtonComponent } from './nested-components/advance-options-button/advance-options-button.component';

import 'ag-grid-enterprise';
import { MessageService } from 'primeng/api';
@Component({
  selector: 'app-rules',
  templateUrl: './rules.component.html',
  styleUrls: ['./rules.component.css']
})
export class RulesComponent {
  private gridApi!: GridApi;

  onGridReady(params: GridReadyEvent) {
    this.gridApi = params.api;
  }
  constructor(
    private DataPreviewDataService:DataPreviewDataService,
    private messageService: MessageService,
    ){

  }
  visible=false;
  currentrow=''
  DatapreviewColumnNames= [
    {field:"Field Names",
    width: 200,
     filter: true,
     sortable: true,
  },
    // {field:"Data Type"},
    {
      field:"Keep column",
    editable: true,
    width: 200,
    cellClass: 'your-custom-class'
    
  }
    ,
    {
      field:"Advanced cleaning options",
      width:300,
      cellClass: 'your-custom-class', 
      cellRenderer: AdvanceOptionsButtonComponent,
      cellRendererParams: {
      clicked: (x:any)=>{
        this.currentrow=x;      
        this.visible=true;
          }
     },


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
  public sideBar:any= ['filters'];
  rowData:any=[]
 
  public defaultColDef: ColDef = {
    initialWidth: 150, 
    resizable: true,
  
   };

   rules:any={
    "columns_kept":[],
    "trim_whitespace":[],
    "remove_special_characters":[],
    "normalize_data":[]
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
      this.messageService.add({ severity: 'success', summary: 'Saved', detail: 'Your rules has been saved' })
   }

   
   ////// cbs

   cb_remove_special_characters=false
   cb_trim_whitespace=false
   cb_normalization=false
   cb_outlierManagement=false;

   setallCBTOFalse(){
    this.cb_remove_special_characters=false;
    this.cb_trim_whitespace=false;
    this.cb_normalization=false;
   }
   savechangestorules(){
  
   if(this.cb_remove_special_characters){
    this.setRemoveSpecialCharacters(this.currentrow);
   }
   if(this.cb_trim_whitespace){
    this.setTrimWhiteSpaces(this.currentrow);
   }
   if(this.cb_normalization){
    this.setNormalization(this.currentrow);
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
   setNormalization(x:any){
    var t1={
      method:''
    }

    t1.method=this.selectedNormalizationTypes
    let temp="{\""+x+"\":"+JSON.stringify(t1)+"}"

    console.log(temp);
    this.rules["normalize_data"].push(JSON.parse(temp));
    console.log(this.rules)
   }


   //////////// data type change
   allowedTypes:any=[{
    types:'ab'}
    ,{types:'bc'}
  ]
   selectedType:any='ab';







   ////////// normalization
   normalizationTypes:any=[{
    types:'min-max'}
    ,{types:'z-score'}
  ]
   selectedNormalizationTypes:any;


   //////outlier Management
   outlierTypes:any=[{
    types:'1 - SD'}
    ,{types:'2 - SD'},
    {types:'3 - SD'}
  ]
  selectedOutlier:any;




  removeAllFields(){
    this.rowData.forEach((x:any)=>{
      x["Keep column"]=false;
       
    })
    this.gridApi.redrawRows();

  }

  addAllFields(){
    this.rowData.forEach((x:any)=>{
      x["Keep column"]=true;
       
    })
    this.gridApi.redrawRows();
  }
   isForceRefreshSelected() {
    return (document.querySelector('#forceRefresh') as HTMLInputElement).checked;
  }
   isSuppressFlashSelected() {
    return (document.querySelector('#suppressFlash') as HTMLInputElement).checked;
  }
}
  


