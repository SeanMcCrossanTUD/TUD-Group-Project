import { Component, ViewChild } from '@angular/core';
import { DataPreviewDataService } from 'src/app/Services/Datacleaning/data-preview-data.service';
import { AgGridAngular } from 'ag-grid-angular';
import { CellClickedEvent, ColDef, GridReadyEvent,GridApi } from 'ag-grid-community';
import { AdvanceOptionsButtonComponent } from './nested-components/advance-options-button/advance-options-button.component';
import { CookieService } from 'ngx-cookie-service';
import 'ag-grid-enterprise';
import { MessageService } from 'primeng/api';
import { HttpClient } from '@angular/common/http';
import { AppSettings, constants } from 'src/app/Const/config';
import { DataCleaningService } from 'src/app/Services/Datacleaning/data-cleaning.service';
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
    private http: HttpClient,
    private CookieService:CookieService,
    private MessageService:MessageService,
    private DataCleaningService:DataCleaningService
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
      field:"cleaning options",
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
  "cleaning options":"abc"

},{'naveen':'abc'}];

  ngOnInit(){

    var id=this.CookieService.get('jobsid');
    this.DataPreviewDataService.getData(id).subscribe(
      (Response)=>{
     
        this.DataPreviewDataService.getJsonData(Response).subscribe(
          (r2:any)=>{           
            this.makedata(r2.columnNames);
            
          }
        )
      },
      (Error)=>{
        this.MessageService.add({ severity: 'error', summary: 'Try again ', detail: "you file is still processing..." });
     
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
          "cleaning options":item
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
    "normalize_data":[],
    "outlier_management":[],
    "missing_value_imputation":[],
    "remove_stopwords":[],
    "label_encoding":[],
    "numerical_column_binning":[],
    "rename_column_name":[],
    "textcase_adjustment":[],
    "replace_substring":[],

    "column_type_conversion":[],
    "text_tokenisation":[],
    "collapse_rare_categories":[],
    "standard_datetime_format":[],
    "regular_expresion_operations":[]
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
      var jobid=this.CookieService.get('jobsid');
      this.DataCleaningService.saveData(this.rules,jobid).subscribe(
        (res)=>{
          this.messageService.add({ severity: 'success', summary: 'Saved', detail: 'Your rules has been saved' })
        },
        (err)=>{
          alert(err);
        }
      )
     
   }

   
   ////// cbs

   cb_remove_special_characters=false
   cb_trim_whitespace=false
   cb_normalization=false
   cb_outlierManagement=false;
   cb_MissingValueImputation=false;
   cb_Numerical_Column_Binning=false;
   cb_Rename_Column_Name=false;
   cb_Text_Case_Adjustment=false;
   cb_Remove_Stopwords=false;
   cb_Replace_Substring=false;
   cb_Label_Encoding=false;

   cb_Column_Type_Conversion=false;
   cb_Text_Tokenisation=false;
   cb_Combine_Rare_Categories=false;
   cb_Standard_Datetime_format=false;
   cb_Regular_Expression_Operations=false;

   setallCBTOFalse(){
    this.cb_remove_special_characters=false
    this.cb_trim_whitespace=false
    this.cb_normalization=false
    this.cb_outlierManagement=false;
    this.cb_MissingValueImputation=false;
    this.cb_Numerical_Column_Binning=false;
    this.cb_Rename_Column_Name=false;
    this.cb_Text_Case_Adjustment=false;
    this.cb_Remove_Stopwords=false;
    this.cb_Replace_Substring=false;
    this.cb_Label_Encoding=false;
    this.cb_Column_Type_Conversion=false;
    this.cb_Text_Tokenisation=false;
    this.cb_Combine_Rare_Categories=false;
    this.cb_Standard_Datetime_format=false;
    this.cb_Regular_Expression_Operations=false;
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
   if(this.cb_outlierManagement){
    this.setOutlierManagement(this.currentrow);
   }
   if(this.cb_MissingValueImputation){
    this.setMissingValueImputation(this.currentrow);
   }
   if(this.cb_Numerical_Column_Binning){
    this.setNumerical_Column_Binning(this.currentrow);
   }
   if(this.cb_Rename_Column_Name){
    this.setRenameColumnName(this.currentrow)
   }
   if(this.cb_Remove_Stopwords){
    this.setRemove_Stopwords(this.currentrow);
   }
   if(this.cb_Label_Encoding){
    this.setLabelEncoding(this.currentrow);
   }
   if(this.cb_Text_Case_Adjustment){
    this.setTextCase(this.currentrow);
   }
   if(this.cb_Replace_Substring){
    this.setReplaceSubstring(this.currentrow);
   }
   if(this.cb_Column_Type_Conversion){
    this.setColumn_Type_Conversion(this.currentrow);
   }
   if(this.cb_Combine_Rare_Categories){
    this.setCombine_Rare_Categories(this.currentrow);
   }
   if(this.cb_Text_Tokenisation){
    this.setText_Tokenisation(this.currentrow);
   }
   if(this.cb_Standard_Datetime_format){
    this.setStandard_Datetime_format(this.currentrow);
   }
   if(this.cb_Regular_Expression_Operations){
    this.setregex(this.currentrow);
   }
   this.visible=false;
   this.currentrow='';
   this.setallCBTOFalse();
   }
/////////////////////////////////////////////
setregex(x:any){
  var json:any;
  if(this.select_Regular_Expression_Operations.types=='Replace'){
    json={
      'columnName':x,
      'method':'Replace',
      'pattern':this.select_Regular_Expression_Operations_from,
      'replaceWith':this.select_Regular_Expression_Operations_to
    }
  }else{
    json={
      'columnName':x,
      'method':'Extract',
      'pattern':this.select_Regular_Expression_Operations_from
    }
  }
  this.rules["regular_expresion_operations"].push(json);
  console.log(this.rules)
}
setStandard_Datetime_format(x:any){
  let temp="{\""+x+"\":\""+this.selected_Standard_Datetime_format+"\"}";
  this.rules["standard_datetime_format"].push(JSON.parse(temp));
  console.log(this.rules)
}
setText_Tokenisation(x:any){
  this.rules["text_tokenisation"].push(x);  
}
setCombine_Rare_Categories(x:any){
  let temp="{\""+x+"\":\""+this.selected_Combine_Rare_Categories+"\"}";
  this.rules["combine_rare_caregories"].push(JSON.parse(temp));
  console.log(this.rules)
}
setColumn_Type_Conversion(x:any){
  let temp="{\""+x+"\":\""+this.select_Column_Type_Conversion.types+"\"}";
  this.rules["column_type_conversion"].push(JSON.parse(temp));
  
}
setReplaceSubstring(x:any){
  let t1="{\""+this.Selected_Replace_Substring_from+"\":\""+this.Selected_Replace_Substring_to+"\"}"
  let temp="{\""+x+"\":"+t1+"}"
  this.rules["replace_substring"].push(JSON.parse(temp));

}
setTextCase(x:any){
 
  let temp="{\""+x+"\":\""+this.select_Text_Case_Adjustment.types+"\"}"
  this.rules["textcase_adjustment"].push(JSON.parse(temp));

}
setRenameColumnName(x:any){
  let temp="{\""+x+"\":\""+this.Selected_Rename_Column_Name+"\"}"
  this.rules["rename_column_name"].push(JSON.parse(temp));
  console.log(this.rules);
}
setNumerical_Column_Binning(x:any){
 
  
  let temp="{\""+x+"\":["+this.values+"]}"

   console.log(temp);
   this.rules["numerical_column_binning"].push(JSON.parse(temp));
}
   setRemove_Stopwords(x:any){
    this.rules["remove_stopwords"].push(x);
   }

   setTrimWhiteSpaces(x:any){
    this.rules["trim_whitespace"].push(x);  
   }
   setRemoveSpecialCharacters(x:any){
    this.rules["remove_special_characters"].push(x);
   }
   setNormalization(x:any){
    var t1={
      method:''
    }

    t1.method=this.selectedNormalizationTypes
    let temp="{\""+x+"\":"+JSON.stringify(t1)+"}"

    console.log(temp);
    this.rules["normalize_data"].push(JSON.parse(temp));
   }

   setOutlierManagement(x:any){
    var t1={
      method:''
    }
    t1.method=this.selectedOutlier;
    let temp="{\""+x+"\":"+JSON.stringify(t1)+"}";
    this.rules["outlier_management"].push(JSON.parse(temp));
   }
   setMissingValueImputation(x:any){
    var t1={
      method:''
    }
    if(this.selectedmissingvalueimpitation.types=="Custom"){
      t1.method=this.Selected_MissingValue_Custom;
    }else{
      t1.method=this.selectedmissingvalueimpitation.types;
    }
    let temp="{\""+x+"\":"+JSON.stringify(t1)+"}";
    this.rules["missing_value_imputation"].push(JSON.parse(temp));

    console.log(this.rules)
   }

   setLabelEncoding(x:any){
    this.rules["label_encoding"].push(x);
   }




   //////////// data type change
   allowedTypes:any=[{
    types:'ab'}
    ,{types:'bc'}
  ]
   selectedType:any='ab';







   ////////// normalization
   normalizationTypes:any=[{
    types:'min-max'},
    {types:'z-score'}
  ]
   selectedNormalizationTypes:any;


   //////outlier Management
   outlierTypes:any=[{
    types:'1 - SD'}
    ,{types:'2 - SD'},
    {types:'3 - SD'}
  ]
  selectedOutlier:any;

  ///// missing value imputation
  MissingValue_Custom=true;
  Selected_MissingValue_Custom:any;
  missingvalueimpitationTypes:any=[{
    types:'Remove'}
    ,{types:'Mode'},
    {types:'Mean'},
    {types:'Median'},
    {types:'Custom'}
  ]
  selectedmissingvalueimpitation:any;

  missingvalueCustom(){
    if(this.selectedmissingvalueimpitation.types=='Custom'){
      this.MissingValue_Custom=false;
    }else{
      this.MissingValue_Custom=true;
    }
  }

  ///////Numerical_Column_Binning
  selected_Numerical_Column_Binning:any;
  values: string[] | undefined;


  ///// column renaming
  Selected_Rename_Column_Name:any;



  ///textcase adjusment
  select_Text_Case_Adjustment:any;
  options_Text_Case_Adjustment:any=[
    {types:'Upper'},
    {types:'Lower'},
    {types:'Title'}
  ]


  /// replace substring
  Selected_Replace_Substring_from:any;
  Selected_Replace_Substring_to:any;
  enableLine(){
   
  }


  // cb_Label_Encoding


  // column type conversion
  options_Column_Type_Conversion:any=[
    {types:'Object'},
    {types:'Text'},
    {types:'Numerical'}
  ]
  select_Column_Type_Conversion:any


  /// combine rare categories

  selected_Combine_Rare_Categories:any=5;


  /// cb_Text_Tokenisation


  //selected_Standard_Datetime_format
  selected_Standard_Datetime_format:any;


  // Regular_Expression_Operations
  select_Regular_Expression_Operations:any;
  options_Regular_Expression_Operations:any=[
    {types:'Replace'},
    {types:'Extract'}
  ]
  select_Regular_Expression_Operations_from:any;
  select_Regular_Expression_Operations_to:any;
  enableReplaceString=false;
  reg(){
    if(this.select_Regular_Expression_Operations.types=='Replace'){
      this.enableReplaceString=true;
    }else{
      this.enableReplaceString=false;
    }
  }
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



  openHelpText(){
  
  }
}


  


