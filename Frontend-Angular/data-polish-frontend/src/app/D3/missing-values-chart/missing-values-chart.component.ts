import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { CookieService } from 'ngx-cookie-service';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';

interface MissingValueData {
  key: string;
  value: number;
}

@Component({
  selector: 'app-missing-values-chart',
  templateUrl: './missing-values-chart.component.html',
  styleUrls: ['./missing-values-chart.component.css']
})
export class MissingValuesChartComponent implements OnInit {
  dataAvailable = false; // Property to track if data is available

  constructor(private D3DashboardService: D3DashboardService,
              private CookieService: CookieService) {}

  ngOnInit() {
    const primarycolor = this.CookieService.get('chartprimarycolor');
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (!data || Object.keys(data.missing_values).length === 0) {
        this.dataAvailable = false;
        return;
      }
      
      this.dataAvailable = true;
      const totalRecords = data.number_of_records;
      const maxBars = 15;
      
      const margin = {top: 10, right: 15, bottom: 100, left: 20};
      const width = 550 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      const svg = d3.select("#chart-missing")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

      if (Object.keys(data.missing_values).length === 0) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("text-anchor", "middle")
            .text("No missing values detected.");
        return;
      }

      const sortedData = Object.entries(data.missing_values)
                               .map(([key, value]): MissingValueData => ({ key, value: Number(value) }))
                               .sort((a, b) => b.value - a.value);

      const displayedData = sortedData.slice(0, maxBars);
      const additionalFields = sortedData.length - maxBars;

      const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
      const y = d3.scaleLinear().rangeRound([height, 0]);

      x.domain(displayedData.map(d => d.key));
      // Use the spread operator to ensure d3.max receives an array
      y.domain([0, d3.max([...displayedData.map(d => d.value)]) || 0]);

      svg.selectAll(".bar")
          .data(displayedData)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", d => x(d.key) || 0)
          .attr("y", d => y(d.value))
          .attr("width", x.bandwidth())
          .attr("height", d => height - y(d.value))
          .style("fill", primarycolor);

      svg.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(d3.axisBottom(x))
          .selectAll("text")
          .attr("transform", "rotate(-55)")
          .style("text-anchor", "end");

      svg.append("g")
          .call(d3.axisLeft(y));

      // Annotation for additional fields
      if (additionalFields > 0) {
        svg.append("text")
           .attr("x", width)
           .attr("y", height + 50)
           .attr("text-anchor", "end")
           .text(`+ ${additionalFields} more fields with missing values`);
      }
    });
  }
}
