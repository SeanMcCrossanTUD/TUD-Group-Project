import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
@Component({
  selector: 'app-number-fields-chart',
  templateUrl: './number-fields-chart.component.html',
  styleUrls: ['./number-fields-chart.component.css']
})


export class NumberFieldsChartComponent implements OnInit {
  number=0;
  constructor(private D3DashboardService:D3DashboardService){

  }
  ngOnInit() {
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }
      this.number=data.number_of_fields;
    });
  }
}