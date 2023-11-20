import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';
import { D3DashboardService } from 'src/app/Services/D3/d3-dashboard.service';
@Component({
  selector: 'app-missing-values-chart',
  templateUrl: './missing-values-chart.component.html',
  styleUrls: ['./missing-values-chart.component.css']
})
export class MissingValuesChartComponent implements OnInit {

  constructor(private D3DashboardService:D3DashboardService){

  }

  ngOnInit() {
this.D3DashboardService.getData().subscribe((data: any) => {
      const totalRecords = data.number_of_records;
    

      const margin = {top: 10, right: 5, bottom: 100, left: 50};
      const width = 500 - margin.left - margin.right;
      const height = 400 - margin.top - margin.bottom;

      const svg = d3.select("#chart-missing")
          .append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
          .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      if (Object.keys(data.missing_values).length === 0) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("text-anchor", "middle")
            .attr("class", "no-data-text")
            .text("No missing values, good job!");
        return;
      }

      const sortedData: [string, number][] = Object.entries(data.missing_values).map(([key, value]) => [key, Number(value)] as [string, number]).sort((a, b) => a[1] - b[1]);
   

      const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
      const y = d3.scaleLinear().rangeRound([height, 0]);

      const tooltip = d3.select("body").append("div")
          .attr("class", "tooltip");

      x.domain(sortedData.map(d => d[0]));
      y.domain([0, d3.max(sortedData, d => d[1] / totalRecords) || 0]);

      svg.selectAll(".bar-1")
          .data(sortedData)
          .enter().append("rect")
          .attr("class", "bar-1")
          .attr("x", d => x(d[0]) || 0)
          .attr("y", height)
          .attr("width", x.bandwidth())
          .attr("height", 0)
          .on("mouseover", function() {
              const d = d3.select(this).data()[0] as [string, number];
              const currentEvent = d3.select(this).node()?.getBoundingClientRect();
              tooltip.transition()
                  .duration(200)
                  .style("opacity", .9);
              tooltip.html(d[0] + ": " + d[1] + " (" + ((d[1] / totalRecords) * 100).toFixed(2) + "%)")
                  .style("left", (currentEvent?.left || 0 + 4) + "px")
                  .style("top", (currentEvent?.top || 0 - 25) + "px");
          })
          .on("mouseout", function() {
              tooltip.transition()
                  .duration(500)
                  .style("opacity", 0);
          })
          .transition()
          .duration(1500)
          .attr("y", d => y(d[1] / totalRecords) || 0)
          .attr("height", d => height - (y(d[1] / totalRecords) || 0));

      // Add the x-axis
      // svg.append("g")
      //     .attr("transform", "translate(0," + height + ")")
      //     .call(d3.axisBottom(x))
      //     .append("text")
      //     .attr("class", "axis-label x-axis-label")
      //     .attr("x", width / 2)
      //     .attr("y", 40)
      //     .attr("transform", "rotate(-55)")
      //     .text("Columns with Missing Values");
      svg.append("g")
          .attr("transform", "translate(0," + height + ")")
          .call(d3.axisBottom(x))
          .selectAll("text")
          .attr("transform", "rotate(-55)")
          .style("text-anchor", "end");

      // Add the y-axis
      svg.append("g")
          .call(d3.axisLeft(y).tickFormat(d => ((d as number) * 100).toFixed(0) + "%"))
          .append("text")
          .attr("class", "axis-label y-axis-label")
          .attr("transform", "rotate(-90)")
          .attr("y", -60)
          .attr("x", -(height / 2))
          .text("% of Missing Values");
    });
  }
}
