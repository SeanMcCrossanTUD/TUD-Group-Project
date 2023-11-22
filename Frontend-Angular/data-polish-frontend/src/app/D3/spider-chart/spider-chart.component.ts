import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-spider-chart',
  templateUrl: './spider-chart.component.html',
  styleUrls: ['./spider-chart.component.css']
})
export class SpiderChartComponent implements OnInit {
  private data = [
    {axis: "Completeness", value: 98},
    {axis: "Uniqueness", value: 60},
    {axis: "Readability", value: 90},
    {axis: "Consistency", value: 99}
  ];

  constructor() { }

  ngOnInit(): void {
    this.createSpiderChart();
  }

  createSpiderChart(): void {
    const width = 300, height = 300;
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const radius = Math.min(width, height) / 2;

    const svg = d3.select('app-spider-chart')
                  .append('svg')
                  .attr('width', width + margin.left + margin.right)
                  .attr('height', height + margin.top + margin.bottom)
                  .append('g')
                  .attr('transform', `translate(${width / 2 + margin.left},${height / 2 + margin.top})`);

    const angleSlice = Math.PI * 2 / this.data.length;
    const rScale = d3.scaleLinear()
                     .range([0, radius])
                     .domain([0, 100]);
    const labelOffset = 20;  // Increase this value if the labels are too close
    const labels = svg.selectAll(".axisLabel")
                                       .data(this.data)
                                       .enter().append("g")
                                       .attr("class", "axisLabel");
                   
    labels.append("text")
                           .attr("class", "legend")
                           .style("font-size", "12px")
                           .attr("text-anchor", "middle")
                           .attr("dy", "0.35em")
                           .attr("x", (d, i) => (rScale(100) + labelOffset) * Math.cos(angleSlice * i - Math.PI / 2))
                           .attr("y", (d, i) => (rScale(100) + labelOffset) * Math.sin(angleSlice * i - Math.PI / 2))
                           .text(d => d.axis);
    // Draw the Circular Grids
    const levels = 5; // Number of levels (concentric circles)
    const levelFactor = radius / levels;

    svg.selectAll(".grid-circle")
       .data(d3.range(1, levels + 1).reverse())
       .enter()
       .append("circle")
       .attr("class", "grid-circle")
       .attr("r", d => levelFactor * d)
       .style("fill", "#CDCDCD")
       .style("stroke", "#CDCDCD")
       .style("fill-opacity", 0.1);

    // Draw the Angular Grid Lines
    svg.selectAll(".axis-line")
       .data(this.data)
       .enter()
       .append("line")
       .attr("class", "axis-line")
       .attr("x1", 0)
       .attr("y1", 0)
       .attr("x2", (d, i) => rScale(100) * Math.cos(angleSlice * i - Math.PI / 2))
       .attr("y2", (d, i) => rScale(100) * Math.sin(angleSlice * i - Math.PI / 2))
       .style("stroke", "black")
       .style("stroke-width", "2px");

    // Transform data to the format expected by d3.radialLine
    const transformedData: [number, number][] = this.data.map((d, i) => {
      return [angleSlice * i, rScale(d.value)] as [number, number];
    });
    

    // Create the radial line function
    const radarLine = d3.radialLine()
        .curve(d3.curveLinearClosed)
        .radius(d => d[1])  // Use the radius (second element of the tuple)
        .angle(d => d[0]);  // Use the angle (first element of the tuple)

    // Append the backgrounds
    svg.append('g')
       .selectAll("path")
       .data([transformedData])  // Use transformed data
       .enter().append("path")
       .attr("d", d => radarLine(d))
       .style("fill", "#f0f0f0")
       .style("fill-opacity", 0.7);

    // Create the outlines 
    svg.append('g')
      .selectAll("path")
      .data([transformedData])  // Use transformed data
      .enter().append("path")
      .attr("d", d => radarLine(d))
      .style("stroke-width", 3)
      .style("stroke", "rgba(255, 165, 0, 0.7)")  // Orange with some transparency
      .style("fill", "rgba(255, 165, 0, 0.2)"); 

    // Draw the axes 
    const axis = svg.selectAll(".axis")
                    .data(this.data)
                    .enter().append("g")
                    .attr("class", "axis");

    axis.append("line")
        .attr("x1", 0)
        .attr("y1", 0)
        .attr("x2", (d, i) => rScale(100) * Math.cos(angleSlice * i - Math.PI / 2))
        .attr("y2", (d, i) => rScale(100) * Math.sin(angleSlice * i - Math.PI / 2))
        .attr("class", "line")
        .style("stroke", "black")
        .style("stroke-width", "2px");

  }
}
