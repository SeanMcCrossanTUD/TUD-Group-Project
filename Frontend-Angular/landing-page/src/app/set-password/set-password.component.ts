import { Component } from '@angular/core';
import { MessageService } from 'primeng/api';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-set-password', 
  templateUrl: './set-password.component.html',
  styleUrl: './set-password.component.css'
})
export class SetPasswordComponent {
  constructor( private messageService:MessageService,
    
    private http:HttpClient){}

  email:any;
  otp:any;
  password1:any;
  password2:any;
  onSubmit(){
    if(!(this.password1==this.password2 && this.password1!=null && this.password1 !==undefined)){
      this.messageService.add({ severity: 'error', summary: 'Check your password', detail: 'make sure to enter same passwords in both box' });
      return;
    }
    if(!(this.otp!=null && this.otp!=undefined && this.email!=null &&  this.email!=undefined)){
      this.messageService.add({ severity: 'error', summary: 'Check your details', detail: 'make sure to enter all details correctly' });
      return;
    }

      this.http.get('http://localhost:8090/set-password?email='+this.email+"&otp="+this.otp+"&newPassword="+this.password1,
      {responseType:'text'})
      .subscribe(
        (res)=>{
          alert('Password has been updated');
          this.showMessage=false;
        },(err)=>{
          console.log(err)
          alert('Invalid OTP')
        }
      )
    console.log()

  }

  showMessage=true;
  navigateToLogin(){

  }
}
