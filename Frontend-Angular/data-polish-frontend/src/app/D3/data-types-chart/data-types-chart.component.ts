import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';

@Component({
  selector: 'app-data-types-chart',
  templateUrl: './data-types-chart.component.html',
  styleUrls: ['./data-types-chart.component.css']
})
export class DataTypesChartComponent implements OnInit {
  dataAvailable: boolean = false;

  constructor(private D3DashboardService: D3DashboardService) {}

  ngOnInit() {
    this.D3DashboardService.getData().subscribe((data: any) => {
      if (data && Object.keys(data.data_type_profile).length > 0) {
        this.dataAvailable = true;
        this.createChart(data);
      } else {
        this.dataAvailable = false;
      }
    });
  }

  createChart(data: any) {
    const margin = { top: 10, right: 10, bottom: 50, left: 50 };
    const width = 250 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;

    const svg = d3.select("#chart-datatypes")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

    const sortedData = Object.entries(data.data_type_profile)
        .map(([key, value]) => [key, Number(value)] as [string, number])
        .sort((a, b) => b[1] - a[1]);

    const x = d3.scaleLinear().rangeRound([0, width]);
    const y = d3.scaleBand().rangeRound([height, 0]).padding(0.1);

    x.domain([0, d3.max(sortedData, d => d[1]) || 0]);
    y.domain(sortedData.map(d => d[0]));

    // Tooltip setup
    let tooltip = d3.select('body').select<HTMLElement>('.tooltip');
    if (tooltip.empty()) {
      tooltip = d3.select('body').append<HTMLElement>('div')
        .attr('class', 'tooltip')
        .style('opacity', 0)
        .style('position', 'absolute')
        .style('text-align', 'center')
        .style('width', '120px')
        .style('height', '28px')
        .style('padding', '2px')
        .style('font', '12px sans-serif')
        .style('background', 'lightsteelblue')
        .style('border', '0px')
        .style('border-radius', '8px')
        .style('pointer-events', 'none');
    }

    svg.selectAll(".bar")
        .data(sortedData)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", 0)
        .attr("y", d => y(d[0]) || 0)
        .attr("width", d => x(d[1]))
        .attr("height", y.bandwidth());

    svg.append("g")
        .attr("transform", `translate(0,${height})`)
        .call(d3.axisBottom(x));

    svg.append("g")
        .call(d3.axisLeft(y))
        .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");
  }
}
