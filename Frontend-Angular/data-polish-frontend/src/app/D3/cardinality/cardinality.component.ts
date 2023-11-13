import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-cardinality',
  templateUrl: './cardinality.component.html',
  styleUrls: ['./cardinality.component.css']
})
export class CardinalityComponent implements OnInit {

  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      const margin = {top: 20, right: 20, bottom: 60, left: 80};
      const width = 960 - margin.left - margin.right;
      const height = 500 - margin.top - margin.bottom;

      const svg = d3.select("#chart")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      if (!data.unique_values_in_text_fields || Object.keys(data.unique_values_in_text_fields).length === 0) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("text-anchor", "middle")
            .attr("class", "no-data-text")
            .text("No cardinality data available.");
        return;
      }

      const sortedData: [string, number][] = Object.entries(data.unique_values_in_text_fields).map(([key, value]) => [key, Number(value)] as [string, number]).sort((a, b) => b[1] - a[1]);
      console.log(sortedData);

      const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
      const y = d3.scaleLinear().rangeRound([height, 0]);

      const tooltip = d3.select("body").append("div")
          .attr("class", "tooltip");

      x.domain(sortedData.map(d => d[0]));
      y.domain([0, d3.max(sortedData, d => d[1]) || 0]);

      svg.selectAll(".bar")
          .data(sortedData)
          .enter().append("rect")
          .attr("class", "bar")
          .attr("x", d => x(d[0]) || 0)
          .attr("y", d => y(d[1]) || 0)
          .attr("width", x.bandwidth())
          .attr("height", d => height - y(d[1]) || 0)
          .on("mouseover", function(event, d) {
              tooltip.transition()
                  .duration(200)
                  .style("opacity", .9);
              tooltip.html(`${d[0]}: ${d[1]}`)
                  .style("left", `${event.pageX}px`)
                  .style("top", `${event.pageY - 28}px`);
          })
          .on("mouseout", function() {
              tooltip.transition()
                  .duration(500)
                  .style("opacity", 0);
          });

      // Add the x-axis
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
          .selectAll("text")
          .attr("transform", "rotate(-45)")
          .style("text-anchor", "end");

      // Add the y-axis
      svg.append("g")
          .call(d3.axisLeft(y))
          .append("text")
          .attr("class", "axis-label y-axis-label")
          .attr("transform", "rotate(-90)")
          .attr("y", -60)
          .attr("x", -(height / 2))
          .text("Cardinality");
    });
  }
}
