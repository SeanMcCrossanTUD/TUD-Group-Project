import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { CookieService } from 'ngx-cookie-service';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';

interface MissingValueData {
  key: string;
  value: number;
  percentage: number;
}

@Component({
  selector: 'app-missing-values-chart',
  templateUrl: './missing-values-chart.component.html',
  styleUrls: ['./missing-values-chart.component.css']
})
export class MissingValuesChartComponent implements OnInit {
  dataAvailable = false;

  constructor(private D3DashboardService: D3DashboardService,
              private CookieService: CookieService) {}

  ngOnInit() {
    const primarycolor = this.CookieService.get('chartprimarycolor');
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (!data || !data.missing_values || Object.keys(data.missing_values).length === 0) {
        this.dataAvailable = false;
        return;
      }

      this.dataAvailable = true;
      const totalRecords = data.number_of_records;
      const maxBars = 15;


      // Explicitly type the value in the filter method
      const filteredData = Object.entries(data.missing_values)
        .filter(([key, value]: [string, any]) => value > 0)
        .map(([key, value]) => ({
          key: key,
          value: Number(value),
          percentage: Number(value) / totalRecords * 100
        }))
        .sort((a, b) => b.value - a.value);

      const displayedData = filteredData.slice(0, maxBars);
      const additionalFields = filteredData.length - maxBars;

      const margin = {top: 10, right: 15, bottom: 100, left: 20};
      const width = 550 - margin.left - margin.right;

      const height = 400 - margin.top - margin.bottom;

      const svg = d3.select("#chart-missing")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", `translate(${margin.left},${margin.top})`);

      const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
      const y = d3.scaleLinear().rangeRound([height, 0]);

      x.domain(displayedData.map(d => d.key));
      y.domain([0, d3.max(displayedData, d => d.value) || 0]);

      let tooltip = d3.select('body').append('div')
        .attr('class', 'tooltip')
        .style('opacity', 0);

      svg.selectAll(".bar")
          .data(displayedData)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", d => x(d.key) || 0)
          .attr("y", d => y(d.value))
          .attr("width", x.bandwidth())
          .attr("height", d => height - y(d.value))
          .style("fill", primarycolor)
          .on('mouseover', function (event, d) {
            tooltip.transition().duration(200).style('opacity', 0.9);
            tooltip.html(`Field: ${d.key}<br/>Missing: ${d.value} (${d.percentage.toFixed(2)}%)`)
              .style('left', (event.pageX) + 'px')
              .style('top', (event.pageY - 28) + 'px');
          })
          .on('mouseout', function () {
            tooltip.transition().duration(500).style('opacity', 0);
          });

      svg.append("g")
          .attr("transform", `translate(0, ${height})`)
          .call(d3.axisBottom(x))
          .selectAll("text")
          .attr("transform", "rotate(-55)")
          .style("text-anchor", "end");

      svg.append("g")
          .call(d3.axisLeft(y));

    //  if (additionalFields > 0) {
    //    svg.append("text")
    //        .attr("x", width - margin.right) 
    //        .attr("y", height - margin.bottom + 50)
    //        .attr("text-anchor", "end")
    //        .text(`+ ${additionalFields} more fields with missing values`);
    //      }
    });
  }
}
