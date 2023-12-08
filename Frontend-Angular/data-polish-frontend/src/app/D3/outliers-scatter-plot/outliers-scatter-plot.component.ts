import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
interface OutlierDataPoint {
  row: number;
  value: number;
  is_outlier: boolean;
  z_score: number;
}

@Component({
  selector: 'app-outliers-scatter-plot',
  templateUrl: './outliers-scatter-plot.component.html',
  styleUrls: ['./outliers-scatter-plot.component.css']
})
export class OutliersScatterPlotComponent implements OnInit {
  private data: any;
  public fields: string[] = [];
  public selectedField: string = '';

  ngOnInit() {
    this.loadData();
  }
  constructor(private D3DashboardService:D3DashboardService){

  }
  loadData() {
    this.D3DashboardService.getoutlier().subscribe(
      (data: any) => {
        console.log(data)
        this.data=data;
      this.fields = data.fields;
      this.selectedField = this.fields[0];
      this.createScatterPlot(this.selectedField);
    });
  
  }


  createScatterPlot(field: string): void {
    d3.select('#scatter-plot').selectAll('*').remove();

    const margin = { top: 20, right: 10, bottom: 30, left: 50 };
    const width = 600 - margin.left - margin.right;
    const height = 500 - margin.top - margin.bottom;

    const svg = d3.select('#scatter-plot')
      .append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const outlierData: OutlierDataPoint[] = this.data.outliers[field];

    const x = d3.scaleLinear()
      .range([0, width])
      .domain(d3.extent(outlierData, d => d.row) as [number, number]);

    const y = d3.scaleLinear()
      .range([height, 0])
      .domain([0, d3.max(outlierData, d => d.value) as number]);

    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(x));

    svg.append('g')
      .call(d3.axisLeft(y));

    const tooltip = d3.select('body').append('div')
      .attr('class', 'tooltip')
      .style('opacity', 0)
      .style('position', 'absolute')
      .style('background', 'white')
      .style('border', '1px solid black')
      .style('padding', '5px')
      .style('pointer-events', 'none');

    svg.selectAll('.dot')
      .data(outlierData)
      .enter().append('circle')
      .attr('class', 'dot')
      .attr('r', 5)
      .attr('cx', d => x(d.row))
      .attr('cy', height)
      .style('fill', d => d.is_outlier ? 'lightcoral' : 'lightblue')
      .style('stroke', 'black')
      .style('stroke-width', '1px')
      .transition()
      .duration(1000)
      .attr('cy', d => y(d.value));

    svg.selectAll('.dot')
      .on('mouseover', function(event, d) {
        const outlierPoint = d as OutlierDataPoint;
        const [px, py] = d3.pointer(event);
        tooltip.transition()
          .duration(200)
          .style('opacity', .9);
        tooltip.html(`Row: ${outlierPoint.row}<br/>Value: ${outlierPoint.value}<br/>Z-Score: ${outlierPoint.z_score}`)
          .style("left", (event.pageX + 10) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on('mouseout', () => {
        tooltip.transition()
          .duration(500)
          .style('opacity', 0);
      });

    // Adding legend
    const legend = svg.append('g')
      .attr('class', 'legend')
      .attr('transform', `translate(${width - 100}, 20)`);

    legend.selectAll(null)
      .data([{color: 'lightcoral', text: 'Outliers'}, {color: 'lightblue', text: 'Regular'}])
      .enter().append('rect')
      .attr('y', (d, i) => i * 20)
      .attr('width', 18)
      .attr('height', 18)
      .style('fill', d => d.color);

    legend.selectAll(null)
      .data([{color: 'lightcoral', text: 'Outliers'}, {color: 'lightblue', text: 'Regular'}])
      .enter().append('text')
      .attr('x', 24)
      .attr('y', (d, i) => i * 20 + 14)
      .text(d => d.text);
  }

  onFieldChange(event: Event): void {
    const target = event.target as HTMLSelectElement;
    this.selectedField = target.value;
    this.createScatterPlot(this.selectedField);
  }  
}
