import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import { HttpClient } from '@angular/common/http';
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

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.loadChartData();
  }
  
  private loadChartData(): void {
    this.http.get<ProcessedDataItem[]>('assets/sample.json').subscribe(data => {
      this.createBubbleChart(data);
    }, error => {
      console.error('Error loading or parsing json data:', error);
    });    
  }
  
  private createBubbleChart(data: ProcessedDataItem[]): void {
    const element = this.chartContainer.nativeElement;
    const svg = d3.select(element).append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom)
      .append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

      const radiusScale = d3.scaleSqrt()
      .domain([0, d3.max(data, (d: ProcessedDataItem) => d.value) ?? 0])
      .range([20, 80]); 

      const simulation = d3.forceSimulation(data)
      .force('charge', d3.forceManyBody().strength(50))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius((node: SimulationNodeDatum) => {
        // Cast the node to ProcessedDataItem
        const item = node as ProcessedDataItem;
        return radiusScale(item.value) + 1;
      }));


    const bubbles = svg.selectAll('.bubble')
      .data(data)
      .enter().append('circle')
      .attr('class', 'bubble')
      .attr('r', (d: ProcessedDataItem) => radiusScale(d.value))
      .attr('fill', () => this.getRandomColor());

    const labels = svg.selectAll('.label')
      .data(data)
      .enter().append('text')
      .attr('class', 'label')
      .attr('text-anchor', 'middle')
      .attr('fill', 'black')
      .text((d: ProcessedDataItem) => d.key)
      .style('font-size', (d: ProcessedDataItem) => {
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
