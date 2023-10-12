import { Component } from '@angular/core';

@Component({
  selector: 'app-data-profile',
  templateUrl: './data-profile.component.html',
  styleUrls: ['./data-profile.component.css']
})
export class DataProfileComponent {
  visible: boolean = false;
  seeimage(e:any){
   alert(e)
   window.open(e);

   

  }
  imgURL=""
  header=""
  showDialog(e:any,c:any) {
    this.imgURL=e;
    this.header=c;
    this.visible = true;
}
}
