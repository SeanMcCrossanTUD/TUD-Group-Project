import { Component, ViewChild } from '@angular/core';
import { BlobStorageService } from '../Services/Fileupload/blob-storage.service';
import { FileUpload } from 'primeng/fileupload';
import { MessageService } from 'primeng/api';
import { CookieService } from 'ngx-cookie-service';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent {
  constructor(
    private BlobStorageService:BlobStorageService,
    private messageService: MessageService,
    private CookieService:CookieService
    ) { }
  model:any={};
  uploadedFiles: any[] = [];
  @ViewChild('fileupload') dropdown!: FileUpload;
  Upload(e:any){
    var jobids: any[]=[];
    try{
      jobids=JSON.parse(this.CookieService.get('jobsid'));
    }catch{    }
    this.dropdown.progress=30;
    for(let file of e.files) {
     
      this.dropdown.progress=50;    
  
      this.BlobStorageService.uploadtoBlob(file).subscribe((respose:any)=>{     

          this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Message Content' });
          this.dropdown.clear();
          jobids.push(respose.jobID);
          this.CookieService.set('jobsid',JSON.stringify(jobids));         
          alert('your job id : ' + respose.jobID);
      },(err)=>{
        console.log(err);
        alert('error uploading file');
       
      });
      this.dropdown.progress=100;
      break;
  }

  }
  onUpload(e:any){
    this.uploadedFiles=[]
  }
}
