const margin = {top: 20, right: 20, bottom: 60, left: 80}; // Adjusted margins to accommodate labels
const width = 960 - margin.left - margin.right;
const height = 500 - margin.top - margin.bottom;

const svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

const x = d3.scaleBand().rangeRound([0, width]).padding(0.1);
const y = d3.scaleLinear().rangeRound([height, 0]);

const tooltip = d3.select("body").append("div")
    .attr("class", "tooltip");

d3.json("results/data_quality_result.json").then(data => {
    const totalRecords = data.number_of_records;
    if (Object.keys(data.missing_values).length === 0) {
        svg.append("text")
            .attr("x", width / 2)
            .attr("y", height / 2)
            .attr("text-anchor", "middle")
            .style("font-size", "24px")
            .style("fill", "#333")
            .text("No missing values, good job!");
        return;
    }

    const sortedData = Object.entries(data.missing_values).sort((a, b) => a[1] - b[1]);

    x.domain(sortedData.map(d => d[0]));
    y.domain([0, d3.max(sortedData, d => d[1] / totalRecords)]);

    svg.selectAll(".bar")
        .data(sortedData)
        .enter().append("rect")
        .attr("class", "bar")
        .attr("x", d => x(d[0]))
        .attr("y", height)
        .attr("width", x.bandwidth())
        .attr("height", 0)
        .on("mouseover", function(d) {
            tooltip.transition()
                .duration(200)
                .style("opacity", .9);
            tooltip.html(d[0] + ": " + d[1] + " (" + ((d[1] / totalRecords) * 100).toFixed(2) + "%)")
                .style("left", (d3.event.pageX + 5) + "px")
                .style("top", (d3.event.pageY - 28) + "px");
        })
        .on("mouseout", function(d) {
            tooltip.transition()
                .duration(500)
                .style("opacity", 0);
        })
        .transition()
        .duration(750)
        .attr("y", d => y(d[1] / totalRecords))
        .attr("height", d => height - y(d[1] / totalRecords));

    // Add the x-axis
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x))
        .append("text") // X-axis Label
        .attr("class", "axis-label")
        .attr("x", width / 2)
        .attr("y", 40)
        .style("text-anchor", "middle")
        .text("Columns with Missing Values");

    // Add the y-axis
    svg.append("g")
        .call(d3.axisLeft(y).tickFormat(d => (d * 100).toFixed(0) + "%"))
        .append("text") // Y-axis Label
        .attr("class", "axis-label")
        .attr("transform", "rotate(-90)")
        .attr("y", -60)
        .attr("x", -(height / 2))
        .style("text-anchor", "middle")
        .text("% of Missing Values");
});
