import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
@Component({
  selector: 'app-records-chart',
  templateUrl: './records-chart.component.html',
  styleUrls: ['./records-chart.component.css']
})
export class RecordsChartComponent implements OnInit {
  number=0;
  constructor(private D3DashboardService:D3DashboardService){

  }
  ngOnInit() {
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      this.number = data.number_of_records; // Assuming this is the value you want to display

      
  }
    )
}
}
