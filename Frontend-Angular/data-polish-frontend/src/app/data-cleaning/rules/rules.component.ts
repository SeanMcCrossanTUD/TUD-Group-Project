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
import { FileUpload } from 'primeng/fileupload';
import { constants2 } from 'src/app/Const/config';
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
    private DataCleaningService:DataCleaningService,
    private constants2:constants2
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
  {field:"Data Type",
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
                  
            this.makedata(r2.columnNames,r2.datatype);
          
            
          }
        )
      },
      (Error)=>{
        this.MessageService.add({ severity: 'error', summary: 'Try again ', detail: "you file is still processing..." });
     
      }
    )

 
    
   
      
  
  }

  makedata(columnNames:any,dtypes:any){
    var temp:any=[];
    for(var i=0;i<columnNames.length;i++){
      console.log(dtypes[i]);
      temp.push(
        {
          "Field Names":columnNames[i],          
          "Data Type":dtypes[i],
          "Keep column":true,
          "cleaning options":columnNames[i]
        }
      )
    }
    // columnNames.forEach((item:any)=>{
    //   temp.push(
    //     {
    //       "Field Names":item,
    //       "Keep column":true,
    //       "cleaning options":item
    //     }
    //   )
    // })
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
    "regular_expresion_operations":[],
    "extract_datetime_components":[],
    "dataset_actions":[]

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
          this.CookieService.set('RULESSAVED','TRUE')
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
   cb_Extract_Datetime_Components=false;
   cb_Remove_Duplicate=false;

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
    this.cb_Extract_Datetime_Components=false;
    this.cb_Remove_Duplicate=false;
    
   }

   resetRules(){
    this.rules={
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
      "regular_expresion_operations":[],
      "extract_datetime_components":[],
      "dataset_actions":[]
  
     }

     this.messageService.add({ severity: 'success', summary: 'Reset Successful ', detail: 'All rules has been reseted' });
     
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
   if(this.cb_Extract_Datetime_Components){
    this.set_Extract_Datetime_Components(this.currentrow);
   }
   this.visible=false;
   this.currentrow='';
   this.setallCBTOFalse();
   console.log(this.rules)
   }

   saveDatasetCleaning(){
    if(this.cb_Remove_Duplicate){
      this.rules['dataset_actions'].push('remove_duplicates')
      
    }
    console.log(this.rules);
    this.cb_Remove_Duplicate=false;
    this.Visibledatasetactions=false;
   }
/////////////////////////////////////////////

set_Extract_Datetime_Components(x:any){
  var json="{\""+x+"\":[";
  var length=this.Extract_Datetime_Components_selected.length;
  for(var i=0;i<length;i++){
    json+="\""+this.Extract_Datetime_Components_selected[i].name+"\""
    if(i+1!=length){
      json+=","
    }
  }
  json+="]}"
 
  this.rules['extract_datetime_components'].push(JSON.parse(json));
  
}
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

}
setStandard_Datetime_format(x:any){
  let temp="{\""+x+"\":\""+this.selected_Standard_Datetime_format.types+"\"}";
  this.rules["standard_datetime_format"].push(JSON.parse(temp));
  
}
setText_Tokenisation(x:any){
  this.rules["text_tokenisation"].push(x);  
}
setCombine_Rare_Categories(x:any){
  let temp="{\""+x+"\":\""+this.selected_Combine_Rare_Categories+"\"}";

  this.rules["collapse_rare_categories"].push(JSON.parse(temp));

}
setColumn_Type_Conversion(x:any){
  console.log(this.select_Column_Type_Conversion)
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
 
}
setNumerical_Column_Binning(x:any){
 
  
  let temp="{\""+x+"\":["+this.values+"]}"


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


    this.rules["normalize_data"].push(JSON.parse(temp));
   }

   setOutlierManagement(x:any){
    var t1={
      method:''
    }
    t1.method=this.selectedOutlier.types;
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
    {types:'Text'},
    {types:'Numerical'}
  ]
  select_Column_Type_Conversion:any


  /// combine rare categories

  selected_Combine_Rare_Categories:any=5;


  /// cb_Text_Tokenisation


  //selected_Standard_Datetime_format
  selected_Standard_Datetime_format:any;

  Standard_Datetime_format_options: any = [
    { types: '%Y-%m-%d' },
    { types: '%d-%m-%Y' },
    { types: '%m-%d-%Y' },
    {types:'%y-%m-%d'},
    {types:'%d-%m-%y'},
    {types:'%m-%d-%y'}
  ];

  // Regular_Expression_Operations
  select_Regular_Expression_Operations:any;
  options_Regular_Expression_Operations:any=[
    {types:'Replace'},
    {types:'Extract'}
  ]
  select_Regular_Expression_Operations_from:any;
  select_Regular_Expression_Operations_to:any;
  enableReplaceString=false;
//////////cb_Extract_Datetime_Components
  Extract_Datetime_Components_selected: any = [];
  Extract_Datetime_Components_options = [
    { name: 'year' },
    { name: 'month' },
    {name:'day'},
    {name:'hour'},
    {name:'minute'},
    {name:'second'},
    
    
  ];
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




  Visibledatasetactions=false;
  dataSetActions(){
    this.Visibledatasetactions=true;
  }

  downloadRules(){
    var jobid=this.CookieService.get('jobsid');
    this.DataCleaningService.downLoadRules(jobid).subscribe(
      (res:any)=>{        
          window.open(this.DataCleaningService.downloadRulesFromBlob(res));
        },
        (err)=>{
          console.log(err);
          this.MessageService.add({ severity: 'error', summary: 'No File Exist / Network issue', detail: "File may not be saved before" });
     
      }
    )
  }

  visibleImportRules=false;
  uploadedFiles: any[] = [];
  @ViewChild('fileupload') dropdown!: FileUpload;
  importRules(){
    this.visibleImportRules=true;
  }

  UploadFile(e:any){
 
    this.dropdown.progress=30;
    var jobID=this.CookieService.get('jobsid');
    for(let file of e.files) {
     
      this.dropdown.progress=50;    
      
      this.DataCleaningService.uploadRules(file,jobID).subscribe((respose:any)=>{     

          this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Your File has been uploaded' });
          this.dropdown.clear();    
          this.visibleImportRules=false;    
          
              
      },(err)=>{

        this.messageService.add({ severity: 'error', summary: 'error', detail: 'Your File not uploaded' });
      
       
      });
      this.dropdown.progress=100;
      break;
  }

  }
  onUploadFile(e:any){
    this.uploadedFiles=[]
  }

  visibleHelpText=false;
  WHAT:any;
  WHY:any;
  EXAMPLE:any;

  openHelpText(element:any){
    console.log(this.constants2.config)
     this.WHAT=this.constants2.config[element].WHAT;
     this.WHY=this.constants2.config[element].WHY;
     this.EXAMPLE=this.constants2.config[element].EXAMPLE;
    this.visibleHelpText=true;
    
  }


  startDataCleaning(){
    var jid=this.CookieService.get('jobsid');
    var url=AppSettings.getBaseURL()+'trigger-cleaning?jobID='+jid;
    this.http.get(url).subscribe(
      (res)=>{
        this.messageService.add({ severity: 'success', summary: 'Cleaning Started with Template', detail: 'Template file uploaded will be used for cleaning dataset.' });
      },(error)=>{
        this.messageService.add({ severity: 'error', summary: 'Something went wrong', detail: 'Your File not uploaded' });
      }
    )
  }
  //// end of class
}


  


