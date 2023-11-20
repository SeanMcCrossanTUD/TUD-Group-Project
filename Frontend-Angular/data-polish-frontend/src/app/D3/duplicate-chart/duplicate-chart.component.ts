import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
@Component({
  selector: 'app-duplicate-chart',
  templateUrl: './duplicate-chart.component.html',
  styleUrls: ['./duplicate-chart.component.css']
})
export class DuplicateChartComponent implements OnInit {

  constructor(private D3DashboardService:D3DashboardService){

  }
  number=0;
  ngOnInit() {
   
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      this.number = data.number_of_duplicate_values; // Assuming this is the value you want to display

    }
    )
  }
}
