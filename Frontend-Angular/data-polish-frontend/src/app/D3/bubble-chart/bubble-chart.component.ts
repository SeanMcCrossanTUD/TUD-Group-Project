import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-bubble-chart',
  templateUrl: './bubble-chart.component.html',
  styleUrls: ['./bubble-chart.component.css']
})
export class BubbleChartComponent implements OnInit {

  private data: any[] = [
    { "id": 1, "category": "Category A", "value1": 10, "value2": 20 },
    { "id": 2, "category": "Category B", "value1": 15, "value2": 25 },
    { "id": 3, "category": "Category C", "value1": 20, "value2": 30 },
    { "id": 4, "category": "Category D", "value1": 25, "value2": 35 }
  ];
  
  private currentColumn: string = 'value1';

  constructor() { }

  ngOnInit(): void {
    this.createBubbleChart();
  }

  private createBubbleChart(): void {
    d3.select('#bubbleChart').selectAll('*').remove();

    const svg = d3.select('#bubbleChart').append('svg')
      .attr('width', 600)
      .attr('height', 400);

    // Create groups for each bubble
    const bubbleGroup = svg.selectAll('.bubble')
      .data(this.data)
      .enter().append('g')
      .attr('class', 'bubble')
      .attr('transform', (d, i) => `translate(${100 + i * 100}, 200)`);

    // Create circles
    bubbleGroup.append('circle')
      .attr('r', d => +d[this.currentColumn])
      .attr('fill', 'steelblue');

    // Create text labels
    bubbleGroup.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '.3em') // Center vertically
      .text(d => d.category); // Replace 'd.category' with the text you want to display

    // Add animation to circles
    bubbleGroup.select('circle').transition()
      .duration(750)
      .attr('r', d => +d[this.currentColumn] * 1.5)
      .transition()
      .duration(750)
      .attr('r', d => +d[this.currentColumn]);
  }

  setColumn(column: string): void {
    this.currentColumn = column;
    this.createBubbleChart();
  }
}
