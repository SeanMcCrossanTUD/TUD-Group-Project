import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

interface CorrelationDataPoint {
  [key: string]: number;
}

@Component({
  selector: 'app-correlation-scatter-plot',
  templateUrl: './correlation-scatter-plot.component.html',
  styleUrls: ['./correlation-scatter-plot.component.css']
})
export class CorrelationScatterPlotComponent implements OnInit {

  private rawData: any; // To store raw data
  private data: CorrelationDataPoint[] = [];
  public fields: string[] = [];
  public selectedTarget: string = '';
  public selectedPredictor: string = '';

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    d3.json('assets/z_score_outliers.json').then((data: any) => {
      this.rawData = data.outliers.outliers;
      this.fields = data.outliers.fields.filter((key: string) => typeof this.rawData[this.fields[0]][0][key] === 'number');
      this.selectedTarget = this.fields[0];
      this.selectedPredictor = this.fields[1];
      this.createScatterPlot();
    });
  }

  createScatterPlot(): void {
    if (!this.selectedTarget || !this.selectedPredictor) {
      return;
    }

    this.data = this.rawData[this.selectedTarget].map((d: any) => ({
      predictor: d[this.selectedPredictor],
      target: d[this.selectedTarget]
    }));

    d3.select('#correlation-plot').selectAll('*').remove();

    const margin = { top: 20, right: 20, bottom: 30, left: 50 },
          width = 960 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

    const svg = d3.select('#correlation-plot')
      .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
      .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d['predictor']) as [number, number])
      .range([0, width]);

    const y = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d['target']) as [number, number])
      .range([height, 0]);

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

    svg.selectAll(".dot")
      .data(this.data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("cx", d => x(d['predictor']))
      .attr("cy", d => y(d['target']))
      .attr("r", 5)
      .style("fill", "#69b3a2")
      .on("mouseover", (event, d) => {
        tooltip.transition().duration(200).style("opacity", 0.9);
        tooltip.html(`Predictor: ${d['predictor']}<br/>Target: ${d['target']}`)
          .style("left", (event.pageX + 10) + "px")
          .style("top", (event.pageY - 28) + "px");
      })
      .on("mouseout", () => {
        tooltip.transition().duration(500).style("opacity", 0);
        tooltip.remove();
      });
  }

  public onFieldChange(): void {
    this.createScatterPlot();
  }
}
