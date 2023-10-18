import { Component } from '@angular/core';

@Component({
  selector: 'app-export',
  templateUrl: './export.component.html',
  styleUrls: ['./export.component.css']
})
export class ExportComponent {

  download(){
    var url="https://fab5storage.blob.core.windows.net/flaskapi2output/clean_data_1697040726.csv"
    window.open(url);
  }
}
