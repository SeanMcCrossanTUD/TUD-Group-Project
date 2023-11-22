import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-data-quality-metric',
  template: '<div id="dq-metric"></div>',
  styleUrls: ['./data-quality-metric.component.css']
})
export class DataQualityMetricComponent implements OnInit {
  private data = [
    { axis: "dq-metric", value: 77 },
  ];

  ngOnInit() {
    this.createChart();
  }

  private createChart(): void {
    const dataset = this.data[0].value / 100;
    const width = 200;
    const height = 200;
    const thickness = 20;

    const color = d3.scaleOrdinal(d3.schemeCategory10);

    const svg = d3.select("#dq-metric")
      .append('svg')
      .attr('class', 'pie')
      .attr('width', width)
      .attr('height', height);

    const arc = d3.arc<d3.PieArcDatum<any>>()
      .innerRadius((width / 2) - thickness)
      .outerRadius(width / 2);

    // Correct the pie value function
    const pie = d3.pie<{value: number}>() // Specify the data type for the pie generator
      .value(d => d.value); // Access the 'value' property of each data object


    const path = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .selectAll('path')
      .data(pie([{value: dataset}, {value: 1 - dataset}])) // Correctly structured data for the pie generator
      .enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d, i) => i === 0 ? color('0') : '#ddd')
      .attr("stroke", "white")
      .attr("stroke-width", "6");


    const text = svg.append("text")
      .text(`${this.data[0].value}%`)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .attr("transform", `translate(${width / 2}, ${height / 2})`)
      .attr("font-size", "30")
      .attr("fill", "#275478");
  }
}
