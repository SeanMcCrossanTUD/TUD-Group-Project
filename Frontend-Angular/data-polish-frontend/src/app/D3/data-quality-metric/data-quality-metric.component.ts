import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { Arc, DefaultArcObject } from 'd3';

@Component({
  selector: 'app-data-quality-metric',
  template: '<div id="dq-metric"></div>',
  styleUrls: ['./data-quality-metric.component.css']
})
export class DataQualityMetricComponent implements OnInit {
  private data = [
    { axis: "dq-metric", value: 77 },
  ];

  ngOnInit() {
    this.createChart();
  }

  private createChart(): void {
    const targetValue = this.data[0].value; // e.g., 77 for 77%
    const dataset = targetValue / 100; // Convert to a scale of 0 to 1
    const width = 200;
    const height = 200;
    const thickness = 20;

    const getColor = (value: number) => {
      return value > 80 ? 'green' : value > 60 ? 'orange' : 'red';
    };

    const svg = d3.select("#dq-metric")
      .append('svg')
      .attr('class', 'pie')
      .attr('width', width)
      .attr('height', height);

    const arcGenerator: Arc<any, DefaultArcObject> = d3.arc()
      .innerRadius((width / 2) - thickness)
      .outerRadius(width / 2);

    const background = svg.append('path')
      .datum({ startAngle: 0, endAngle: 2 * Math.PI } as DefaultArcObject)
      .style('fill', '#ddd')
      .attr('d', arcGenerator)
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

    const foreground = svg.append('path')
      .datum({ startAngle: 0, endAngle: 0 } as DefaultArcObject)
      .style('fill', getColor(targetValue))
      .attr('d', arcGenerator)
      .attr('transform', `translate(${width / 2}, ${height / 2})`);

      foreground.transition()
      .duration(1500)
      .attrTween('d', (d: DefaultArcObject) => {
        const interpolate = d3.interpolate(d.endAngle, 2 * Math.PI * dataset);
        return (t) => {
          d.endAngle = interpolate(t);
          return arcGenerator(d) || '';
        };
      });

    const text = svg.append('text')
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .attr('font-size', '40')
      .attr('fill', getColor(targetValue))
      .text('0%');

    text.transition()
      .duration(1500)
      .tween('text', function () {
        const that = d3.select(this);
        const i = d3.interpolateNumber(0, targetValue);
        return function (t) {
          that.text(Math.round(i(t)) + '%');
        };
      });
  }
}
