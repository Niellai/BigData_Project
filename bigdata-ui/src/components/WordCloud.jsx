import React, { useEffect } from "react";
import * as d3 from "d3";
import cloud from "d3-cloud";

const WordCloud = ({ data, containerWidth }) => {
  const width = containerWidth ? containerWidth : 500;
  const height = containerWidth ? containerWidth : 500;
  const fill = d3.scaleOrdinal(d3.schemeCategory10);

  useEffect(() => {
    const draw = (words) => {
      d3.select(".cloud")
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr(
          "transform",
          "translate(" + (width * 9) / 20 + "," + (height * 11) / 20 + ")"
        )
        .selectAll("text")
        .data(words)
        .enter()
        .append("text")
        .style("font-size", 1)
        .style("font-family", "Impact")
        .style("fill", function (d, i) {
          return fill(i);
        })
        .transition()
        .duration(500)
        .style("font-size", function (d) {
          return d.size + "px";
        })
        .attr("text-anchor", "middle")
        .attr("transform", function (d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function (d) {
          return d.text;
        });
    };

    cloud()
      .size([width, height])
      .words(
        Object.keys(data).map((d) => {
          return { text: d, size: data[d] * 1.25, test: "haha" };
        })
      )
      .padding(5)
      .rotate(function () {
        return ~~(Math.random() * 4) * 45;
      })
      .font("Impact")
      .fontSize(function (d) {
        return d.size;
      })
      .on("end", draw)
      .start();
  }, [width, data, height, fill]);

  return <div className="cloud"></div>;
};

export default WordCloud;
