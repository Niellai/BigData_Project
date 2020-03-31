import React, { useEffect } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";
import sampleData from "../data/sampleWordcloud";

const WordCloud = () => {
  const width = 500;
  const height = 500;
  const fill = d3.scaleOrdinal(d3.schemeCategory10);

  const draw = words => {
    d3.select(".cloud")
      .append("svg")
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")")
      .selectAll("text")
      .data(words)
      .enter()
      .append("text")
      .style("font-size", 1)
      .style("font-family", "Impact")
      .style("fill", function(d, i) {
        return fill(i);
      })
      .transition()
      .duration(500)
      .style("font-size", function(d) {
        return d.size + "px";
      })
      .attr("text-anchor", "middle")
      .attr("transform", function(d) {
        return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
      })
      .text(function(d) {
        return d.text;
      });
  };

  var layout = cloud()
    .size([500, 500])
    .words(
      sampleData.map(function(d) {
        return { text: d, size: 10 + Math.random() * 90, test: "haha" };
      })
    )
    .padding(5)
    .rotate(function() {
      return ~~(Math.random() * 4) * 45;
    })
    .font("Impact")
    .fontSize(function(d) {
      return d.size;
    })
    .on("end", draw);

  useEffect(() => {
    layout.start();
  }, []);

  return <div className="cloud"></div>;
};

export default WordCloud;
