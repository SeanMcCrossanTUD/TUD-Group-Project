import { Component, ViewChild } from '@angular/core';
import { BlobStorageService } from '../Services/Fileupload/blob-storage.service';
import { FileUpload } from 'primeng/fileupload';
import { MessageService } from 'primeng/api';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent {
  constructor(private BlobStorageService:BlobStorageService,private messageService: MessageService) { }
  model:any={};
  uploadedFiles: any[] = [];
  @ViewChild('fileupload') dropdown!: FileUpload;
  Upload(e:any){
    this.dropdown.progress=30;
    for(let file of e.files) {
      this.dropdown.progress=50;
      this.BlobStorageService.uploadtoBlob(file).subscribe((respose:any)=>{
      
      },(err)=>{
        this.messageService.add({ severity: 'success', summary: 'Success', detail: 'Message Content' });
        this.dropdown.clear();
      });
      this.dropdown.progress=100;
      break;
  }

  }
  onUpload(e:any){
    this.uploadedFiles=[]
  }
}
