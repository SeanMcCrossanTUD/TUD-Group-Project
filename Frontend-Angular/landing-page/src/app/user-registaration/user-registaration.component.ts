import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
@Component({
  selector: 'app-user-registaration', 
  templateUrl: './user-registaration.component.html',
  styleUrl: './user-registaration.component.css'
})
export class UserRegistarationComponent {
  constructor(private http:HttpClient,
      private messageService:MessageService
    ){
  }
  ngOnInit(){
    // this.http
    // .post('https://prod-46.northeurope.logic.azure.com:443/workflows/643dcc1efa6a41908dd2846b226a0ffd/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9LE2z3sTd7ucTVWRYu2K-TuRPi1MT1pk_LLR5KSjIo8',{
    //   'EMAILID':'d22124491@mytudublin.ie',
    //   'OTP':'1234'
    // }).subscribe(
    //   (res)=>{
    //     console.log(res);
    //   }
    // )
  }
  userName:any;
  email:any;
  
  onSubmit(){
  
    var regex=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
   
    
    if(!(this.email!='' &&
     this.email!=undefined 
      && regex.test(this.email))){
        this.messageService.add({ severity: 'error', summary: 'Check your Email', detail: 'Please enter correct email' });
        return;
      }

      if(!(this.userName!='' &&
     this.userName!=undefined )
     ){
        this.messageService.add({ severity: 'error', summary: 'Check your user name', detail: 'Please enter user name ' });
        return;
      }

      

  }
}
