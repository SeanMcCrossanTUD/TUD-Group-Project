import { Component, OnInit, ElementRef, ViewChild } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';

interface BubbleDataItem extends d3.SimulationNodeDatum {
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
  categories: string[] = [];
  selectedCategory: string = '';

  constructor(private D3DashboardService: D3DashboardService) { }

  ngOnInit(): void {
    this.D3DashboardService.getBubbleChart().subscribe(data => {
      this.categories = Object.keys(data.value_counts);
      this.selectedCategory = this.categories[0];
      const bubbleData = this.transformData(data.value_counts[this.selectedCategory]);
      this.createBubbleChart(bubbleData);
    }, error => {
      console.error('Error loading json data:', error);
    });
  }

  onCategoryChange(category: string): void {
    this.selectedCategory = category;
    if (category) {
      this.D3DashboardService.getBubbleChart().subscribe(data => {
        const bubbleData = this.transformData(data.value_counts[category]);
        this.createBubbleChart(bubbleData);
      });
    }
  }

  private transformData(data: any): BubbleDataItem[] {
    return Object.entries(data).map(([key, value]) => ({
      key: key,
      value: value as number
    }));
  }

  private createBubbleChart(data: BubbleDataItem[]): void {
    d3.select(this.chartContainer.nativeElement).select('svg').remove();
    const element = this.chartContainer.nativeElement;
    const svg = d3.select(element).append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom)
      .append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

    const radiusScale = d3.scaleSqrt()
      .domain([0, d3.max(data, d => d.value) ?? 0])
      .range([20, 80]);

    const simulation = d3.forceSimulation(data)
      .force('charge', d3.forceManyBody().strength(50))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(d => radiusScale(d.value) + 1));

    const tooltip = d3.select('body').append('div')
      .attr('class', 'bubble-tooltip')
      .style('opacity', 0);

    const bubbles = svg.selectAll('.bubble')
      .data(data)
      .enter().append('circle')
      .attr('class', 'bubble')
      .attr('r', d => radiusScale(d.value))
      .attr('fill', this.getRandomColor())
      .on('mouseover', (event, d) => {
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html(`Key: ${d.key}<br/>Value: ${d.value}`)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 28) + 'px');
      })
      .on('mouseout', () => {
        tooltip.transition().duration(500).style('opacity', 0);
        tooltip.remove();
      });

    simulation.on('tick', () => {
      bubbles.attr('cx', d => d.x ?? 0).attr('cy', d => d.y ?? 0);
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
