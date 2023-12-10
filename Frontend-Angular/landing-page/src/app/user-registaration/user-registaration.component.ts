import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { Router } from '@angular/router';
@Component({
  selector: 'app-user-registaration', 
  templateUrl: './user-registaration.component.html',
  styleUrl: './user-registaration.component.css'
})
export class UserRegistarationComponent {
  constructor(private http:HttpClient,
      private messageService:MessageService,
      private router:Router
    ){
  }

  goHome(){
    this.router.navigate(["/"]);
  }
  ngOnInit(){
    
  }
  userName:any;
  email:any;
  showMessage=true;
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


      

  


 
      // Make the first HTTP POST request to 'http://localhost:8090/user-register'
      this.http.post('http://localhost:8090/user-register?fullName='+this.userName+"&email="+this.email,{}).subscribe(
        (res1: any) => {
          // Assuming 'res1' contains the OTP, adjust the property accordingly
          const otp = res1;
  
          // Make the second HTTP POST request to the Azure Logic App
          this.http.post('https://prod-46.northeurope.logic.azure.com:443/workflows/643dcc1efa6a41908dd2846b226a0ffd/triggers/manual/paths/invoke?api-version=2016-10-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=9LE2z3sTd7ucTVWRYu2K-TuRPi1MT1pk_LLR5KSjIo8', {
            'EMAILID': this.email,
            'OTP': otp
          }).subscribe(
            (res) => {
              this.showMessage=true;
            },
            (error) => {
              this.messageService.add({ severity: 'error', summary: 'Check your details', detail: 'something went wrong' });
            }
          );
        },
        (error1) => {
          this.messageService.add({ severity: 'error', summary: 'Check your details', detail: 'something went wrong' });
        }
      );
    }
    
      

  
}
