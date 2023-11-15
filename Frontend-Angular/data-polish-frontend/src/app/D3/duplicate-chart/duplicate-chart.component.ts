import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-duplicate-chart',
  templateUrl: './duplicate-chart.component.html',
  styleUrls: ['./duplicate-chart.component.css']
})
export class DuplicateChartComponent implements OnInit {
  number=0;
  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      this.number = data.number_of_duplicate_values; // Assuming this is the value you want to display

    }
    )
  }
}
