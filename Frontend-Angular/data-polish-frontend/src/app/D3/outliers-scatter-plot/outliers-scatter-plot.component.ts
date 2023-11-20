import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { pointer } from 'd3';

@Component({
  selector: 'app-outliers-scatter-plot',
  templateUrl: './outliers-scatter-plot.component.html',
  styleUrls: ['./outliers-scatter-plot.component.css']
})
export class OutliersScatterPlotComponent implements OnInit {

  private data: any; // Holds the loaded data
  fields!: string[];
  selectedField!: string;

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    d3.json('assets/data.json').then(data => {
      this.data = data;
      this.fields = Object.keys(this.data.z_score_outliers);
      this.selectedField = this.fields[0];
      this.createScatterPlot(this.selectedField);
    });
  }

  createScatterPlot(field: string): void {
    d3.select('#scatter-plot').selectAll('*').remove();

    const margin = { top: 20, right: 20, bottom: 30, left: 50 };
    const width = 960 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const svg = d3.select('#scatter-plot')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleLinear()
      .range([0, width])
      .domain(d3.extent(this.data.z_score_outliers[field], (d: any) => +d.row) as [number, number]);

    const y = d3.scaleLinear()
      .range([height, 0])
      .domain([0, d3.max(this.data.z_score_outliers[field], (d: any) => +d.value) as number]);

    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .call(d3.axisLeft(y));

    const tooltip = d3.select('#scatter-plot').append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0);

    svg.selectAll('.dot')
      .data(this.data.z_score_outliers[field])
      .enter().append('circle')
      .attr('class', 'dot')
      .attr('r', 5)
      .attr('cx', (d: any) => x(+d.row))
      .attr('cy', (d: any) => y(+d.value))
      .style('fill', (d: any) => d.is_outlier ? 'red' : 'blue')
      .on('mouseover', (event, d: any) => {
        const [x, y] = pointer(event);
        tooltip.transition()
          .duration(200)
          .style('opacity', .9);
        tooltip.html(`Row: ${d.row}<br/>Value: ${d.value}<br/>Z-Score: ${d.z_score}`)
          .style('left', `${x}px`)
          .style('top', `${y - 28}px`);
      })
      .on('mouseout', () => {
        tooltip.transition()
          .duration(500)
          .style('opacity', 0);
      });
  }

  onFieldChange(event: Event): void {
    const target = event.target as HTMLSelectElement;
    this.selectedField = target.value;
    this.createScatterPlot(this.selectedField);
  }
}
