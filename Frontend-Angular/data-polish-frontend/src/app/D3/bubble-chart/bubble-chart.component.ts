import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import { SimulationNodeDatum } from 'd3';

interface ProcessedDataItem extends SimulationNodeDatum {
  key: string;
  value: number;
}

@Component({
  selector: 'app-bubble-chart',
  templateUrl: './bubble-chart.component.html',
  styleUrls: ['./bubble-chart.component.css']
})
export class BubbleChartComponent implements OnInit {
  @ViewChild('bubbleChart', { static: true }) private chartContainer!: ElementRef;
  private margin = { top: 40, right: 20, bottom: 30, left: 40 };
  private width = 600 - this.margin.left - this.margin.right;
  private height = 400 - this.margin.top - this.margin.bottom;
  private data: string[] = ['dog', 'cat', 'cat', 'cat', 'dog', 'frog', 'cat'];

  constructor() { }

  ngOnInit(): void {
    this.createBubbleChart();
  }

  private createBubbleChart(): void {
    const element = this.chartContainer.nativeElement;
    const dataProcessed: ProcessedDataItem[] = this.processData(this.data);

    const svg = d3.select(element).append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom)
      .append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

    const radiusScale = d3.scaleSqrt()
      .domain([0, d3.max(dataProcessed, (d: ProcessedDataItem) => d.value) ?? 0])
      .range([20, 80]); // Adjusted range for larger bubbles
  
    const simulation = d3.forceSimulation(dataProcessed as ProcessedDataItem[])
      .force('charge', d3.forceManyBody().strength(50)) // Increased strength for more repulsion
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius((d: SimulationNodeDatum) => {
        const item = d as ProcessedDataItem;
        return radiusScale(item.value) + 1; // Add a small value to ensure separation
      }))
      .on('tick', ticked); // Add the tick function
      
    function ticked() {
        bubbles
          .attr('cx', d => d.x ?? 0)
          .attr('cy', d => d.y ?? 0);
    
        labels
          .attr('x', d => d.x ?? 0)
          .attr('y', d => (d.y ?? 0) + 5);
      }

    const bubbles = svg.selectAll('.bubble')
      .data(dataProcessed)
      .enter().append('circle')
      .attr('class', 'bubble')
      .attr('r', (d: ProcessedDataItem) => radiusScale(d.value))
      .attr('fill', () => this.getRandomColor());

    const labels = svg.selectAll('.label')
      .data(dataProcessed)
      .enter().append('text')
      .attr('class', 'label')
      .attr('text-anchor', 'middle')
      .attr('fill', 'black') // Change to black for better contrast or any color that suits your design
      .text((d: ProcessedDataItem) => d.key)
      .style('font-size', (d: ProcessedDataItem) => {
        // Ensure a minimum font size, for example, 10px
        const minFontSize = 20;
        const calculatedSize = Math.min(2 * radiusScale(d.value), (2 * radiusScale(d.value) - 8) / this.getWidth(d.key));
        return `${Math.max(minFontSize, calculatedSize)}px`;
      })
      .style('pointer-events', 'none');

    simulation.on('tick', () => {
      bubbles
        .attr('cx', d => d.x ?? 0)
        .attr('cy', d => d.y ?? 0);

      labels
        .attr('x', d => d.x ?? 0)
        .attr('y', d => (d.y ?? 0) + 5);
    });
  }

  private processData(data: string[]): ProcessedDataItem[] {
    const counts: { [key: string]: number } = {};
    data.forEach(item => {
      counts[item] = (counts[item] || 0) + 1;
    });
    return Object.keys(counts).map(key => ({
      key,
      value: counts[key]
    }));
  }

  private getRandomColor(): string {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
      color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
  }

  private getWidth(text: string): number {
    return text.length * 6;
  }
}
