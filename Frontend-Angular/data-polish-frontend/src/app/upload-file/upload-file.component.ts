import { Component, ViewChild } from '@angular/core';
import { BlobStorageService } from '../Services/Fileupload/blob-storage.service';
import { FileUpload } from 'primeng/fileupload';
import { MessageService } from 'primeng/api';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';
import { fadeInAnimation } from '../Animations/animation';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css'],
  animations: [fadeInAnimation],
  host: { '[@fadeInAnimation]': '' }
})
export class UploadFileComponent {
  constructor(
    private BlobStorageService:BlobStorageService,
    private messageService: MessageService,
    private CookieService:CookieService,
    private router:Router
    ) { }
  model:any={};
  uploadedFiles: any[] = [];
  @ViewChild('fileupload') dropdown!: FileUpload;
  Upload(e:any){
 
    this.dropdown.progress=30;
    for(let file of e.files) {
     
      this.dropdown.progress=50;    
  
      this.BlobStorageService.uploadtoBlob(file).subscribe((respose:any)=>{     

          this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Your File has been uploaded' });
          this.dropdown.clear();         
          this.CookieService.set('jobsid',respose.jobID);  
       
          this.router.navigate([2]);
              
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
