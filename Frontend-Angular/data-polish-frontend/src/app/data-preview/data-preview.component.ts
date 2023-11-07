import { Component } from '@angular/core';
import { DataPreviewDataService } from '../Services/Datacleaning/data-preview-data.service';
import { fadeInAnimation } from '../Animations/animation';
@Component({
  selector: 'app-data-preview',
  templateUrl: './data-preview.component.html',
  styleUrls: ['./data-preview.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class DataPreviewComponent {

  constructor(private DataPreviewDataService:DataPreviewDataService){

  }
  DatapreviewColumnNames=[]
  DatapreviewData=[];

  ngOnInit(){
    this.DataPreviewDataService.getData().subscribe(
      (response:any)=>{
        this.DatapreviewColumnNames=response.coloumnNames;
        this.DatapreviewData=response.data;
      }
    )


   
  
  }
  

}
