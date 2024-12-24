
import React, { useEffect, useState } from "react";
import api from "./services/api";

const App = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await api.get("/");
        setMessage(response.data.message);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div>
      <h1>React + FastAPI</h1>
      <p>{message}</p>
    </div>
  );
};

export default App;
