import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-dq-chart', // Updated selector
  templateUrl: './data-quality-metric.component.html',
  styleUrls: ['./data-quality-metric.component.css']
})
export class DataQualityMetricComponent implements OnInit {
  @ViewChild('chart', { static: true }) private chartContainer!: ElementRef; // Updated ViewChild selector

  private data = [
    { axis: "dq-metric", value: 77 },
  ];

  ngOnInit() {
    this.createChart();
  }

  private createChart(): void {
    const element = this.chartContainer.nativeElement;
    const svg = d3.select(element).append('svg')
      .attr('width', 200)
      .attr('height', 200);

    const margin = 10;
    const width = +svg.attr('width') - margin * 2;
    const height = +svg.attr('height') - margin * 2;
    const radius = Math.min(width, height) / 2;
    const percentComplete = this.data[0].value / 100; // Convert to a fraction

    const progress = svg.append('g')
      .attr('transform', `translate(${width / 2 + margin}, ${height / 2 + margin})`);

    // Background circle
    progress.append('circle')
      .attr('cx', 0)
      .attr('cy', 0)
      .attr('r', radius)
      .style('fill', '#e6e6e6');

    // Foreground arc
    const endAngle = 2 * Math.PI * percentComplete;
    const x1 = radius * Math.sin(endAngle);
    const y1 = -radius * Math.cos(endAngle);
    
    const pathData = `M 0 -${radius} A ${radius} ${radius} 0 ${endAngle > Math.PI ? 1 : 0} 1 ${x1} ${y1}`;
    
    progress.append('path')
      .attr('d', pathData)
      .style('fill', '#00f');

    // Text in the middle
    progress.append('text')
      .text(`${this.data[0].value}%`)
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .style('font-size', '20px')
      .style('fill', '#000');
  }
}
