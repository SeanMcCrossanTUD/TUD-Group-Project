import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { HttpClient } from '@angular/common/http';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
interface SpiderData {
  axis: string;
  value: number;
}

@Component({
  selector: 'app-spider-chart',
  templateUrl: './spider-chart.component.html',
  styleUrls: ['./spider-chart.component.css']
})
export class SpiderChartComponent implements OnInit {

  constructor(private http: HttpClient,
    private D3DashboardService:D3DashboardService) { }

  ngOnInit(): void {
    this.fetchData();
  }

  private fetchData(): void {
    this.D3DashboardService.getQualityMertic().subscribe(data => {
      if (data) {
        const spiderData: SpiderData[] = [
          { axis: "Completeness", value: parseFloat((data.completeness_score * 100).toFixed(2)) },
          { axis: "Uniqueness", value: parseFloat((data.uniqueness_score * 100).toFixed(2)) },
          { axis: "Readability", value: parseFloat((data.average_readability * 100).toFixed(2)) },
          { axis: "Consistency", value: parseFloat((data.consistency_score * 100).toFixed(2)) }
        ];
        this.createSpiderChart(spiderData);
      }
    });
  }

  private createSpiderChart(data: SpiderData[]): void {
    const width = 400, height = 300;
    const margin = { top: 50, right: 50, bottom: 50, left: 50 };
    const radius = Math.min(width, height) / 2;
    const angleSlice = Math.PI * 2 / data.length;
    const rScale = d3.scaleLinear().range([0, radius]).domain([0, 100]);

    const svg = d3.select('#app-spider-chart')
                  .append('svg')
                  .attr('width', width + margin.left + margin.right)
                  .attr('height', height + margin.top + margin.bottom)
                  .append('g')
                  .attr('transform', `translate(${width / 2 + margin.left},${height / 2 + margin.top})`);

    // Create labels
    const labels = svg.selectAll(".axisLabel")
                      .data(data)
                      .enter().append("g")
                      .attr("class", "axisLabel");
                   
    labels.append("text")
          .attr("class", "legend")
          .style("font-size", "12px")
          .attr("text-anchor", "middle")
          .attr("dy", "0.35em")
          .attr("x", (d, i) => (rScale(100) + 20) * Math.cos(angleSlice * i - Math.PI / 2))
          .attr("y", (d, i) => (rScale(100) + 20) * Math.sin(angleSlice * i - Math.PI / 2))
          .text(d => d.axis);

    // Create grid circles
    svg.selectAll(".grid-circle")
       .data(d3.range(1, 6).reverse())
       .enter()
       .append("circle")
       .attr("class", "grid-circle")
       .attr("r", d => radius / 5 * d)
       .style("fill", "#CDCDCD")
       .style("stroke", "#CDCDCD")
       .style("fill-opacity", 0.1);

    // Create radar line
    const radarLine = d3.radialLine<SpiderData>()
                        .curve(d3.curveLinearClosed)
                        .radius(d => rScale(d.value))
                        .angle((d, i) => i * angleSlice);

    svg.append('path')
       .datum(data)
       .attr('d', radarLine)
       .style('fill', '#69b3a2')
       .style('fill-opacity', 0.7);

    // Create axes
    svg.selectAll(".axis")
       .data(data)
       .enter()
       .append("line")
       .attr("x1", 0)
       .attr("y1", 0)
       .attr("x2", (d, i) => rScale(100) * Math.cos(angleSlice * i - Math.PI / 2))
       .attr("y2", (d, i) => rScale(100) * Math.sin(angleSlice * i - Math.PI / 2))
       .style("stroke", "black")
       .style("stroke-width", "2px");
  }
}
