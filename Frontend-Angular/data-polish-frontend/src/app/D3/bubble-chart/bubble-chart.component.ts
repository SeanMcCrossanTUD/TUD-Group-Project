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
  public numberOfInstances: number = 0;

  constructor(private D3DashboardService: D3DashboardService) { }

  ngOnInit(): void {
    this.D3DashboardService.getBubbleChart().subscribe(data => {
      this.categories = Object.keys(data.value_counts);
      this.selectedCategory = this.categories[0];
      const bubbleData = this.transformData(data.value_counts[this.selectedCategory]);
      this.calculateTotalValue(bubbleData);
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

  private totalValue: number = 0;

  private calculateTotalValue(data: BubbleDataItem[]): void {
    this.totalValue = data.reduce((acc, item) => acc + item.value, 0);
}

  private createBubbleChart(data: BubbleDataItem[]): void {
    d3.select(this.chartContainer.nativeElement).select('svg').remove();
    const element = this.chartContainer.nativeElement;
    this.numberOfInstances = data.length;

    const svg = d3.select(element).append('svg')
      .attr('width', this.width + this.margin.left + this.margin.right)
      .attr('height', this.height + this.margin.top + this.margin.bottom);

    const chartLayer = svg.append('g')
      .attr('transform', `translate(${this.margin.left},${this.margin.top})`);

    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 5])
      .on('zoom', (event) => {
        chartLayer.attr('transform', event.transform);
      });
  
    svg.call(zoom as any);

    const radiusScale = d3.scaleSqrt()
      .domain([0, d3.max(data, d => d.value) ?? 0])
      .range([20, 80]);

    const simulation = d3.forceSimulation(data)
      .force('charge', d3.forceManyBody().strength(50))
      .force('center', d3.forceCenter(this.width / 2, this.height / 2))
      .force('collision', d3.forceCollide().radius(d => radiusScale((d as BubbleDataItem).value) + 1));

    const tooltip = d3.select('body').append('div')
      .attr('class', 'bubble-tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'white')
      .style('border', '1px solid black')
      .style('padding', '5px')
      .style('pointer-events', 'none')
      .style('z-index', '10');

    const bubbles = chartLayer.selectAll('.bubble')
      .data(data)
      .enter().append('circle')
      .attr('class', 'bubble')
      .attr('r', d => radiusScale(d.value))
      .attr('fill', 'lightblue')
      .style("stroke", "black")
      .style("stroke-width", "2px");

    const labels = chartLayer.selectAll('.bubble-label')
      .data(data)
      .enter().append('text')
      .attr('class', 'bubble-label')
      .style('text-anchor', 'middle')
      .style('fill', 'black')
      .text(d => d.key)
      .style('pointer-events', 'none')
      .attr('dy', '0.35em'); // Adjust for vertical centering

    simulation.on('tick', () => {
      bubbles.attr('cx', d => (d as BubbleDataItem).x ?? 0)
             .attr('cy', d => (d as BubbleDataItem).y ?? 0);

      labels.attr('x', d => (d as BubbleDataItem).x ?? 0)
            .attr('y', d => (d as BubbleDataItem).y ?? 0);
    });

    bubbles.on('mouseover', (event, d) => {
      d3.select(event.currentTarget)
        .attr('fill', 'lightcoral');
    
      // Calculate relative value (e.g., as a percentage)
      const relativeValue = (d.value / this.totalValue) * 100;
    
      tooltip.transition().duration(200).style('opacity', 0.9);
      tooltip.html(`Key: ${d.key}<br/>Absolute Value: ${d.value}<br/>Relative Value: ${relativeValue.toFixed(2)}%`)
        .style('left', (event.pageX + 10) + 'px')
        .style('top', (event.pageY - 28) + 'px');
    })
    .on('mouseout', (event) => {
      d3.select(event.currentTarget)
        .attr('fill', 'lightblue');
    
      tooltip.transition().duration(500).style('opacity', 0);
    });


      svg.selectAll('.bubble-label')
      .data(data)
      .enter().append('text')
      .attr('class', 'bubble-label')
      .style('text-anchor', 'middle')
      .style('fill', 'black')
      .text(d => d.key)
      .style('pointer-events', 'none')
      .attr('dy', '.3em') // Vertically center align
      .each(function(d) {
        const node = d3.select(this);
        const radius = radiusScale(d.value);
        node.attr('x', d.x ?? 0)
            .attr('y', d.y ?? 0);
      });

    simulation.on('tick', () => {
      bubbles.attr('cx', d => (d as BubbleDataItem).x ?? 0)
             .attr('cy', d => (d as BubbleDataItem).y ?? 0);
      svg.selectAll('.bubble-label')
         .attr('x', d => (d as BubbleDataItem).x ?? 0)
         .attr('y', d => ((d as BubbleDataItem).y ?? 0));
    });
}
}
