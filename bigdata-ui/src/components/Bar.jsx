import React from "react";
import { ResponsiveBarCanvas } from "@nivo/bar";
// make sure parent container have a defined height when using
// responsive component, otherwise height will be 0 and
// no chart will be rendered.
// website examples showcase many properties,
// you'll often use just a few of them.
const MyResponsiveBarCanvas = ({ data /* see data tab */ }) => (
  <ResponsiveBarCanvas
    data={data}
    keys={[
      "hot dog",
      "burger",
      "sandwich",
      "kebab",
      "fries",
      "donut",
      "junk",
      "sushi",
      "ramen",
      "curry",
      "udon",
      "bagel",
      "yakitori",
      "takoyaki",
      "tacos",
      "miso soup",
      "tortilla",
      "tapas",
      "chipirones",
      "gazpacho",
      "soba",
      "bavette",
      "steak",
      "pizza",
      "spaghetti",
      "ravioli",
      "salad",
      "pad thai",
      "bun",
      "waffle",
      "crepe",
      "churros",
      "paella",
      "empanadas",
      "bruschetta",
      "onion soup",
      "cassoulet",
      "bouillabaisse",
      "unagi",
      "tempura",
      "tonkatsu",
      "shabu-shabu",
      "twinkies",
      "jerky",
      "fajitas",
      "jambalaya",
      "meatloaf",
      "mac n' cheese",
      "baked beans",
      "popcorn",
      "buffalo wings",
      "BBQ ribs",
      "apple pie",
      "nachos",
      "risotto",
      "tiramisu"
    ]}
    indexBy="country"
    margin={{ top: 50, right: 60, bottom: 50, left: 60 }}
    pixelRatio={1}
    padding={0.15}
    innerPadding={0}
    minValue="auto"
    maxValue="auto"
    groupMode="stacked"
    layout="horizontal"
    reverse={false}
    colors={{ scheme: "red_blue" }}
    colorBy="id"
    borderWidth={0}
    borderColor={{ from: "color", modifiers: [["darker", 1.6]] }}
    axisTop={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "",
      legendOffset: 36
    }}
    axisRight={null}
    axisBottom={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "country",
      legendPosition: "middle",
      legendOffset: 36
    }}
    axisLeft={{
      tickSize: 5,
      tickPadding: 5,
      tickRotation: 0,
      legend: "food",
      legendPosition: "middle",
      legendOffset: -40
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

export default MyResponsiveBarCanvas;
