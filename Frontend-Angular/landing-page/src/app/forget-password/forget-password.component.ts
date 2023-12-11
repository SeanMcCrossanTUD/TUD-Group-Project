import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MessageService } from 'primeng/api';
@Component({
  selector: 'app-forget-password', 
  templateUrl: './forget-password.component.html',
  styleUrl: './forget-password.component.css'
})
export class ForgetPasswordComponent {
  showMessage=true;
  constructor(  private router:Router,
    private messageService:MessageService,
    private http:HttpClient){}
  goHome(){
    this.router.navigate(["/"]);
  }
  email:any;
  onSubmit(){

    var regex=/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
   
    
    if(!(this.email!='' &&
     this.email!=undefined 
      && regex.test(this.email))){
        this.messageService.add({ severity: 'error', summary: 'Check your Email', detail: 'Please enter correct email' });
        return;
      }
    
      this.http.get('http://16.170.150.247:8090/forget-password?email='+this.email,
        {responseType:'text'}
      )
      .subscribe(
        (Response:any)=>{
          this.http.post('https://prod-46.northeurope.logic.azure.com:443/workflows/643dcc1efa6a41908dd2846b226a0ffd/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9LE2z3sTd7ucTVWRYu2K-TuRPi1MT1pk_LLR5KSjIo8', {
            'EMAILID': this.email,
            'OTP': Response
          }).subscribe(
            (res) => {
              this.showMessage=false;
            },
            (error) => {
              this.messageService.add({ severity: 'error', summary: 'Check your details', detail: 'something went wrong' });
            }
          )
        },
        (error:any)=>{
          console.log(error);
        }
      )


  }
}
