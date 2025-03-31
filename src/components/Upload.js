import { useState } from "react";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");

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
  };

  return (
    <div className="flex flex-col items-center">
      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
        className="p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 transition"
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 text-white px-4 py-2 mt-3 rounded-lg hover:bg-blue-700 transition"
      >
        Upload & Analyze
      </button>
      {prediction && (
        <p className="mt-4 bg-gray-200 text-lg p-2 rounded-lg shadow-md">
          Result: <span className="font-semibold">{prediction}</span>
        </p>
      )}
    </div>
  );
};

export default Upload;
