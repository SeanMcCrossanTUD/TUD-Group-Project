import { Component, OnInit } from '@angular/core';
import * as d3 from 'd3';

@Component({
  selector: 'app-number-fields-chart',
  templateUrl: './number-fields-chart.component.html',
  styleUrls: ['./number-fields-chart.component.css']
})


export class NumberFieldsChartComponent implements OnInit {

  ngOnInit() {
    console.log('Component ngOnInit called');
    d3.json("assets/data_quality_result.json").then((data: any) => {
      if (!data) {
        console.error('Data is undefined');
        return;
      }

      const numberToDisplay = data.number_of_fields; // Assuming this is the value you want to display

      const svg = d3.select("#chart-number")
          .append("svg")
          .attr("width", 300) // Adjust width as needed
          .attr("height", 200); // Adjust height as needed

      // Add text to the SVG
      svg.append("text")
          .attr("x", 150) // Center the text (adjust as needed)
          .attr("y", 100) // Adjust the position as needed
          .attr("text-anchor", "middle")
          .style("font-size", "48px") // Adjust font size as needed
          .text(numberToDisplay);
    });
  }
}