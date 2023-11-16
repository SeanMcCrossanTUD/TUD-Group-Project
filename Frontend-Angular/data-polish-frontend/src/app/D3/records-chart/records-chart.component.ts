import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-records-chart',
  templateUrl: './records-chart.component.html',
  styleUrls: ['./records-chart.component.css']
})
export class RecordsChartComponent implements OnInit {
  number=0;
  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      this.number = data.number_of_records; // Assuming this is the value you want to display

      
  }
    )
}
}
