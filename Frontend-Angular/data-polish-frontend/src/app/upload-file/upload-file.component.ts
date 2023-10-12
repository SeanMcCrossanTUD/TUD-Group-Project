import { Component } from '@angular/core';
import { BlobStorageService } from '../Services/Fileupload/blob-storage.service';
@Component({
  selector: 'app-upload-file',
  templateUrl: './upload-file.component.html',
  styleUrls: ['./upload-file.component.css']
})
export class UploadFileComponent {
  constructor(private BlobStorageService:BlobStorageService) { }
  model:any={};
  uploadFile(e:any){
    this.model.file=e.target.files[0];
    this.model.name=e.target.files[0].name;
  }
  upload(){
   
    this.BlobStorageService.uploadtoBlob(this.model);
  }
  uploadedFiles: any[] = [];
  onUpload(e:any){
    for(let file of e.files) {
      this.uploadedFiles.push(file);
  }

  }
}
