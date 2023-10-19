import { Component ,ViewChild} from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'app-data-profile',
  templateUrl: './data-profile.component.html',
  styleUrls: ['./data-profile.component.css']
})
export class DataProfileComponent {
  visible: boolean = false;
  items: MenuItem[] | undefined;
  @ViewChild('img') img!: any;
  @ViewChild('newwindow') newwindow!:any;
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

ngOnInit() {
  this.items = [
      { label: 'Download',command:()=>this.funcc() }
     // { label: 'Delete', icon: 'pi pi-fw pi-trash' }
  ];
}

funcc(){
  
  window.open(this.imgURL);
}
}
