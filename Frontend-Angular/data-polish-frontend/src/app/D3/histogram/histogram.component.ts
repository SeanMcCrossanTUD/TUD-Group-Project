import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

interface HistogramDataPoint {
  value: number;
}

@Component({
  selector: 'app-histogram',
  templateUrl: './histogram.component.html',
  styleUrls: ['./histogram.component.css']
})
export class HistogramComponent implements OnInit {
  private rawData: any;
  private data: HistogramDataPoint[] = []; 
  public fields: string[] = []; 
  public selectedField: string = ''; 

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    d3.json('assets/z_score_outliers.json').then((data: any) => {
      this.rawData = data.outliers.outliers;
      this.fields = data.outliers.fields;

      if (this.fields.length > 0) {
        this.selectedField = this.fields[0];
        this.createHistogram();
      } else {
        console.error('No fields found');
      }
    }).catch(error => {
      console.error('Error loading data:', error);
    });
  }

  createHistogram(): void {
    if (!this.selectedField) {
      return;
    }

    // Filter data for the selected field and ensure values are defined
    this.data = this.rawData[this.selectedField]
                  .filter((d: any) => d.value !== undefined)
                  .map((d: any) => ({ value: d.value }));

    d3.select('#histogram').selectAll('*').remove();

    const margin = { top: 10, right: 30, bottom: 30, left: 40 },
          width = 460 - margin.left - margin.right,
          height = 400 - margin.top - margin.bottom;

    const svg = d3.select("#histogram")
      .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", `translate(${margin.left}, ${margin.top})`);

    const x = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d.value) as [number, number])
      .range([0, width]);
    svg.append("g")
      .attr("transform", `translate(0, ${height})`)
      .call(d3.axisBottom(x));

    const histogram = d3.histogram<HistogramDataPoint, number>()
      .value(d => d.value)
      .domain(x.domain() as [number, number])
      .thresholds(x.ticks(40)); // Adjust the number of bins

    const bins = histogram(this.data);

    const y = d3.scaleLinear()
      .range([height, 0])
      .domain([0, d3.max(bins, bin => bin.length) as number]);
    svg.append("g")
      .call(d3.axisLeft(y));

    svg.selectAll("rect")
      .data(bins)
      .enter()
      .append("rect")
        .attr("x", 1)
        .attr("transform", d => `translate(${x(d.x0 as number)}, ${y(d.length)})`)
        .attr("width", d => x(d.x1 as number) - x(d.x0 as number) - 1)
        .attr("height", d => height - y(d.length))
        .style("fill", "#69b3a2");
    // Normal distribution curve
    const mean = d3.mean(this.data, d => d.value) as number;
    const deviation = d3.deviation(this.data, d => d.value) as number;
    const normalLine = d3.line<HistogramDataPoint>()
      .curve(d3.curveBasis)
      .x(d => x(d.value))
      .y(d => {
        const pdf = (1 / (deviation * Math.sqrt(2 * Math.PI))) *
                    Math.exp(-0.5 * Math.pow((d.value - mean) / deviation, 2));
        return y(pdf * height); // Adjust pdf value to fit histogram's y scale
      });

    const normalData = x.ticks(100).map(val => ({ value: val }));

    svg.append("path")
      .datum(normalData)
      .attr("fill", "none")
      .attr("stroke", "green")
      .attr("stroke-width", 2)
      .attr("d", normalLine);

        const line = d3.line<d3.Bin<HistogramDataPoint, number>>()
        .curve(d3.curveBasis)
        .x(d => x((d.x0! + d.x1!) / 2)) // Using non-null assertion operator
        .y(d => y(d.length));
    
      svg.append("path")
        .datum(bins)
        .attr("fill", "none")
        .attr("stroke", "red")
        .attr("stroke-width", 1.5)
        .attr("d", line);
  }

  public onFieldChange(): void {
    this.createHistogram();
  }
}
