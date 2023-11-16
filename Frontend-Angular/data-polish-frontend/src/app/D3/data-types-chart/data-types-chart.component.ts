import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-data-types-chart',
  templateUrl: './data-types-chart.component.html',
  styleUrls: ['./data-types-chart.component.css']
})
export class DataTypesChartComponent implements OnInit {

  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      console.log(data);

      const margin = {top: 10, right: 10, bottom: 50, left: 50};
      const width = 250 - margin.left - margin.right;
      const height = 300 - margin.top - margin.bottom;

      const svg = d3.select("#chart-datatypes")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      if (Object.keys(data.data_type).length === 0) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("text-anchor", "middle")
            .attr("class", "no-data-text")
            .text("No data!");
        return;
      }

      const sortedData: [string, number][] = Object.entries(data.data_type).map(([key, value]) => [key, Number(value)] as [string, number]).sort((a, b) => a[1] - b[1]);
      console.log(sortedData);

      // Swap the x and y scales
      const x = d3.scaleLinear().rangeRound([0, width]);
      const y = d3.scaleBand().rangeRound([height, 0]).padding(0.1);

      const tooltip = d3.select("body").append("div")
          .attr("class", "tooltip");

      // Update domains for the rotated chart
      x.domain([0, d3.max(sortedData, d => d[1]) || 0]);
      y.domain(sortedData.map(d => d[0]));

      svg.selectAll(".bar")
          .data(sortedData)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", 0)
          .attr("y", d => y(d[0]) || 0)
          .attr("width", d => x(d[1]))
          .attr("height", y.bandwidth())
          .on("mouseover", function() {
              const d = d3.select(this).data()[0] as [string, number];
              const currentEvent = d3.select(this).node()?.getBoundingClientRect();
              tooltip.transition()
                  .duration(200)
                  .style("opacity", .9);
              tooltip.html(d[0] + ": " + d[1])
                  .style("left", (currentEvent?.left || 0) + "px")
                  .style("top", (currentEvent?.top || 0) - 28 + "px");
          })
          .on("mouseout", function() {
              tooltip.transition()
                  .duration(500)
                  .style("opacity", 0);
          });

      // Add the y-axis
      svg.append("g")
          .call(d3.axisLeft(y));

      // Add the x-axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
          .append("text")
          .attr("class", "axis-label x-axis-label")
          .attr("x", width / 2)
          .attr("y", 40)
          .text("Count of Data Types");

      // Rotate the text on the y-axis if it's too long
      svg.selectAll(".y-axis .tick text")
          .attr("transform", "rotate(-45)")
          .style("text-anchor", "end");
    });
  }
}
