import fetch from "node-fetch";

export const convertDate = (date) => {
  const isoDate = date.toISOString();
  const formattedDate = isoDate.split("T")[0].split("-").reverse().join("-");
  return formattedDate;
};

export const getWordCloud = async (start_date, end_date) => {
  try {
    const baseUrl = process.env.REACT_APP_BASEURL;
    const body = { start_date, end_date };
    const response = await fetch(`${baseUrl}/WordCloud`, {
      method: "post",
      body: JSON.stringify(body),
      headers: { "Content-Type": "application/json" },
    });
    const rjson = await response.json();
    return rjson;
  } catch (error) {
    console.log(error);
    return {};
  }
};