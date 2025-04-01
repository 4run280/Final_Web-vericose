import { useState } from "react";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [reportUrl, setReportUrl] = useState("");

  const handleUpload = async () => {
    if (!file) return alert("Please select a file.");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/upload", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setPrediction(data.prediction);
    setConfidence(data.confidence);
    setReportUrl(data.report_url);
  };

  return (
    <div className="flex flex-col items-center">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="p-2 border border-gray-300 rounded-lg"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 mt-3 rounded-lg"
      >
        Upload & Analyze
      </button>
      {prediction && (
        <p className="mt-4 bg-gray-200 text-lg p-2 rounded-lg">
          Result: {prediction} ({confidence.toFixed(2)}%)
        </p>
      )}
      {reportUrl && (
        <a href={reportUrl} download className=" text-white px-4 py-2 mt-3 rounded-lg">
          Download Report
        </a>
      )}
    </div>
  );
};

export default Upload;
