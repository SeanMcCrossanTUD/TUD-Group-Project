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
    this.numberOfInstances = data.length;
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
      .force('collision', d3.forceCollide().radius(d => radiusScale((d as BubbleDataItem).value) + 1));

      const tooltip = d3.select('body').append('div')
      .attr('class', 'bubble-tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'white')
      .style('border', '1px solid black')
      .style('padding', '5px')
      .style('pointer-events', 'none')
      .style('z-index', '10'); // Ensure tooltip is on top
    
      const bubbles = svg.selectAll('.bubble')
      .data(data)
      .enter().append('circle')
      .attr('class', 'bubble')
      .attr('r', d => radiusScale(d.value))
      .attr('fill', 'lightblue') // Original color
      .style("stroke", "black")
      .style("stroke-width", "2px")
      .on('mouseover', (event, d) => {
        d3.select(event.currentTarget) // Select the current bubble
          .attr('fill', 'lightcoral'); // Change color to light red on hover
  
        tooltip.transition().duration(200).style('opacity', 0.9);
        tooltip.html(`Key: ${d.key}<br/>Value: ${d.value}`)
          .style('left', (event.pageX + 10) + 'px')
          .style('top', (event.pageY - 28) + 'px');
      })
      .on('mouseout', (event) => {
        d3.select(event.currentTarget) // Select the current bubble
          .attr('fill', 'lightblue'); // Revert color back to light blue
  
        tooltip.transition().duration(500).style('opacity', 0);
      });
    

    // Adding labels to bubbles
    svg.selectAll('.bubble-label')
      .data(data)
      .enter().append('text')
      .attr('class', 'bubble-label')
      .style('text-anchor', 'middle')
      .style('fill', 'black')
      .text(d => d.key)
      .style('pointer-events', 'none');

      simulation.on('tick', () => {
        bubbles.attr('cx', d => (d as BubbleDataItem).x ?? 0)
               .attr('cy', d => (d as BubbleDataItem).y ?? 0);
      
        svg.selectAll('.bubble-label')
           .attr('x', d => (d as BubbleDataItem).x ?? 0)
           .attr('y', d => ((d as BubbleDataItem).y ?? 0) + 5); // Adjust y position to align text in the center of the bubble
      });
  }
}
