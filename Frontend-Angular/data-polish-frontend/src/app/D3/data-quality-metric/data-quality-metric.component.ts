import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { arc, pie, PieArcDatum } from 'd3-shape';

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
    const dataset = { score: this.data[0].value / 100 };
    const width = 200;
    const height = 200;
    const thickness = 20;

    const getColor = (score: number) => {
      if (score > 0.8) return 'green';
      else if (score > 0.6) return 'orange';
      else return 'red';
    };

    const svg = d3.select("#dq-metric")
      .append('svg')
      .attr('class', 'pie')
      .attr('width', width)
      .attr('height', height);

    const arcGenerator = arc<PieArcDatum<any>>()
      .innerRadius((width / 2) - thickness)
      .outerRadius(width / 2);

    const pieGenerator = pie<any>()
      .value((d: any) => d.score)
      .sort(null);

    const pathData = pieGenerator([{ score: 0 }, { score: 1 - dataset.score }]);

    const path = svg.append('g')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .selectAll('path')
      .data(pathData)
      .enter()
      .append('path')
      .attr('d', arcGenerator as any) // cast to 'any' to avoid type errors
      .attr('fill', (d, i) => i === 0 ? getColor(dataset.score) : '#ddd')
      .attr('stroke', 'white')
      .attr('stroke-width', '6');

    path.data(pieGenerator([{ score: dataset.score }, { score: 1 - dataset.score }]))
      .transition()
      .duration(1500)
      .attrTween('d', function (d) {
        const i = d3.interpolateNumber(0, d.value as number);
        return function (t) {
          d.value = i(t);
          return arcGenerator(d as PieArcDatum<any>) as unknown as string;
        };
      });

    const text = svg.append('text')
      .text(`0%`)
      .attr('text-anchor', 'middle')
      .attr('dominant-baseline', 'middle')
      .attr('transform', `translate(${width / 2}, ${height / 2})`)
      .attr('font-size', '40')
      .attr('fill', getColor(dataset.score));

    text.transition()
      .duration(1500)
      .tween('text', function () {
        const that = d3.select(this);
        const i = d3.interpolateNumber(0, dataset.score * 100);
        return function (t) {
          that.text(Math.round(i(t)) + '%');
        };
      });
  }
}
