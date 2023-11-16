import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-number-fields-chart',
  templateUrl: './number-fields-chart.component.html',
  styleUrls: ['./number-fields-chart.component.css']
})


export class NumberFieldsChartComponent implements OnInit {
  number=0;
  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }
      this.number=data.number_of_fields;
    });
  }
}