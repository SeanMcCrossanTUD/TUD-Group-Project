import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Arc, DefaultArcObject } from 'd3';
import { HttpClient } from '@angular/common/http';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
@Component({
  selector: 'app-uniqueness-metric',
  templateUrl: './uniqueness-metric.component.html',
  styleUrls: ['./uniqueness-metric.component.css']
})
export class UniquenessMetricComponent implements OnInit {
  dataAvailable = false;

  constructor(private http: HttpClient,
    private D3DashboardService:D3DashboardService) {}

  ngOnInit() {
    this.fetchData();
  }

  private fetchData(): void {
    this.D3DashboardService.getQualityMertic().subscribe(data => {
      if (data && data.uniqueness_score !== undefined) {
        const roundedUniqueness = parseFloat(data.uniqueness_score.toFixed(2));
        this.createChart(roundedUniqueness * 100); // Convert to percentage
        this.dataAvailable = true;
      }
    });
  }

  private createChart(uniqueness: number): void {
    const dataset = uniqueness / 100;
    const width = 150;
    const height = 150;
    const thickness = 15;

    const getColor = (value: number) => {
      return value > 80 ? 'green' : value > 60 ? 'orange' : 'red';
    };

    const svg = d3.select("#uniqueness")
      .append('svg')
      .attr('class', 'pie')
      .attr('width', width)
      .attr('height', height);

    const arcGenerator: Arc<any, DefaultArcObject> = d3.arc()
      .innerRadius((width / 2) - thickness)
      .outerRadius(width / 2);

    svg.append('path')
      .datum({ startAngle: 0, endAngle: 2 * Math.PI } as DefaultArcObject)
      .style('fill', '#ddd')
      .attr('d', arcGenerator)
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const foreground = svg.append('path')
      .datum({ startAngle: 0, endAngle: 0 } as DefaultArcObject)
      .style('fill', getColor(uniqueness))
      .attr('d', arcGenerator)
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    foreground.transition()
      .duration(1500)
      .attrTween('d', (d: DefaultArcObject) => {
        const interpolate = d3.interpolate(d.endAngle, 2 * Math.PI * dataset);
        return (t: number) => {
          d.endAngle = interpolate(t);
          return arcGenerator(d) || '';
        };
      });

    const text = svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .attr('font-size', '40')
      .attr('fill', getColor(uniqueness))
      .text('0%');

    text.transition()
      .duration(1500)
      .tween('text', function () {
        const that = d3.select(this);
        const i = d3.interpolateNumber(0, uniqueness);
        return function (t) {
          that.text(Math.round(i(t)) + '%');
        };
      });
  }
}
