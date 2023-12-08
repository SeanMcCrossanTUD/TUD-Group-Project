import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { CookieService } from 'ngx-cookie-service';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
interface CorrelationDataPoint {
  predictor: number;
  target: number;
}

@Component({
  selector: 'app-correlation-scatter-plot',
  templateUrl: './correlation-scatter-plot.component.html',
  styleUrls: ['./correlation-scatter-plot.component.css']
})
export class CorrelationScatterPlotComponent implements OnInit {
  private rawData: any;
  private data: CorrelationDataPoint[] = [];
  public fields: string[] = [];
  public selectedTarget: string = '';
  public selectedPredictor: string = '';

  ngOnInit() {
    this.loadData();
  }
  constructor(private D3DashboardService:D3DashboardService,
    private cookieService:CookieService){

  }

  loadData() {
    this.D3DashboardService.getoutlier().subscribe(
      (data: any) => {
        console.log(data)
      this.rawData = data.outliers;
      this.fields = data.fields;
  
      if (this.fields.length >= 2) {
        this.selectedTarget = this.fields[0];
        this.selectedPredictor = this.fields[1];
        this.createScatterPlot();
      } else {
        console.error('Insufficient numeric fields found');
      }
    },
    (error)=>{
      console.error('Error loading data:', error);
    }
    );
  }

  createScatterPlot(): void {
    if (!this.selectedTarget || !this.selectedPredictor) {
      return; // Exit if fields are not selected
    }

    // Prepare data for plotting
    this.data = this.rawData[this.selectedTarget].map((d: any) => ({
      predictor: d.value,
      target: this.rawData[this.selectedPredictor].find((p: any) => p.row === d.row)?.value
    })).filter((d: any) => d.target !== undefined);

    d3.select('#correlation-plot').selectAll('*').remove();

    const margin = { top: 20, right: 10, bottom: 30, left: 50 },
          width = 600 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;

    const svg = d3.select('#correlation-plot')
      .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
      .append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    // X axis
    const x = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d.predictor) as [number, number])
      .range([0, width]);
    svg.append('g')
      .attr('transform', `translate(0, ${height})`)
      .call(d3.axisBottom(x));

    // Y axis
    const y = d3.scaleLinear()
      .domain(d3.extent(this.data, d => d.target) as [number, number])
      .range([height, 0]);
    svg.append('g')
      .call(d3.axisLeft(y));

    // Tooltip
    const tooltip = d3.select('body').append('div')
      .attr('class', 'tooltip')
      .style('opacity', 70)
      .style('position', 'absolute')
      .style('background', 'white')
      .style('border', '1px solid black')
      .style('padding', '5px')
      .style('pointer-events', 'none');

    // Data points
    var primarycolor=this.cookieService.get("chartprimarycolor");
    const circles = svg.selectAll(".dot")
      .data(this.data)
      .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 5)
      .attr("cx", 0) // Start from the left
      .attr("cy", d => y(d.target))
      .style("fill", "lightblue") // Lighter fill color
      .style("stroke", "black") // Hard border
      .style("stroke-width", "2px"); // Border width

    // Transition for moving from the left to the right
    circles.transition()
      .duration(1000)
      .attr("cx", d => x(d.predictor));

    circles.on("mouseover", (event, d) => {
      tooltip.transition().duration(200).style("opacity", 0.9);
      tooltip.html(`Predictor: ${d.predictor}<br/>Target: ${d.target}`)
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
