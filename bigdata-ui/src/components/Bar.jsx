import React from "react";
import { ResponsiveBarCanvas } from "@nivo/bar";
// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.
const MyResponsiveBarCanvas = ({ data }) => {
  const { barData, keyData } = data;
  return (
    <ResponsiveBarCanvas
      data={barData}
      keys={keyData}
      indexBy="index"
      margin={{ top: 50, right: 60, bottom: 50, left: 60 }}
      pixelRatio={1}
      padding={0.15}
      innerPadding={0}
      minValue="auto"
      maxValue="auto"
      groupMode="stacked"
      layout="horizontal"
      reverse={false}
      colors={{ scheme: "yellow_green_blue" }}
      colorBy="id"
      borderWidth={0}
      borderColor={{ from: "color", modifiers: [["darker", 1.6]] }}
      axisTop={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "",
        legendOffset: 36,
      }}
      axisRight={null}
      axisBottom={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "count",
        legendPosition: "middle",
        legendOffset: 36,
      }}
      axisLeft={{
        tickSize: 5,
        tickPadding: 5,
        tickRotation: 0,
        legend: "words",
        legendPosition: "middle",
        legendOffset: -40,
      }}
      enableGridX={true}
      enableGridY={false}
      enableLabel={true}
      labelSkipWidth={12}
      labelSkipHeight={12}
      labelTextColor={{ from: "color", modifiers: [["darker", 1.6]] }}
      isInteractive={true}
    />
  );
};

export default MyResponsiveBarCanvas;
