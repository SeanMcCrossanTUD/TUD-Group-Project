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
  
    const getColor = (value: number) => {
      if (value > 80) return 'green';
      else if (value > 60) return 'orange';
      else return 'red';
    };
  
    const svg = d3.select("#dq-metric")
      .append('svg')
      .attr('class', 'pie')
      .attr('width', width)
      .attr('height', height);
  
    const arc = d3.arc<d3.PieArcDatum<any>>()
      .innerRadius((width / 2) - thickness)
      .outerRadius(width / 2);
  
    const pie = d3.pie<{ value: number }>()
      .value(d => d.value);
  
    const path = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .selectAll('path')
      .data(pie([{ value: dataset }, { value: 1 - dataset }]))
      .enter()
      .append("path")
      .attr("d", arc)
      .attr("fill", (d, i) => i === 0 ? getColor(this.data[0].value) : '#ddd')
      .attr("stroke", "white")
      .attr("stroke-width", "6");
  
    const text = svg.append("text")
      .text(`${this.data[0].value}%`)
      .attr("text-anchor", "middle")
      .attr("dominant-baseline", "middle")
      .attr("transform", `translate(${width / 2}, ${height / 2})`)
      .attr("font-size", "40")
      .attr("fill", getColor(this.data[0].value));
  }  
}
