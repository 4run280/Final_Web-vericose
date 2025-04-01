// Upload.jsx
import { useState } from "react";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [confidence, setConfidence] = useState(null);
  const [reportUrl, setReportUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    try {
      if (!file) {
        setError("Please select a file.");
        return;
      }

      setIsLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || `HTTP error! status: ${response.status}`);
      }

      if (data.success) {
        setPrediction(data.prediction);
        setConfidence(data.confidence);
        setReportUrl(`http://127.0.0.1:5000${data.report_url}`);
        setError(null);
      } else {
        throw new Error(data.error || 'Unknown error occurred');
      }

    } catch (error) {
      console.error("Upload error:", error);
      setError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col items-center p-4">
      <div className="w-full max-w-md">
        <input
          type="file"
          onChange={(e) => {
            setFile(e.target.files[0]);
            setError(null);
          }}
          accept="image/*"
          className="w-full p-2 border border-gray-300 rounded-lg mb-4"
        />
        
        <button
          onClick={handleUpload}
          disabled={!file || isLoading}
          className={`w-full py-2 px-4 rounded-lg ${
            isLoading 
              ? 'bg-gray-400 cursor-wait' 
              : file 
                ? 'bg-blue-600 text-white hover:bg-blue-700' 
                : 'bg-gray-400 text-gray-200 cursor-not-allowed'
          }`}
        >
          {isLoading ? 'Processing...' : 'Upload & Analyze'}
        </button>

        {error && (
  <div className="mt-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded max-w-full break-words">
    <div className="font-bold mb-1">Error:</div>
    <div className="text-sm whitespace-pre-wrap overflow-auto max-h-32">
      {error.replace(/\\\\/g, '\\').replace(/Detection failed: Detection failed:/g, 'Detection failed:')}
    </div>
  </div>
)}
        
        {prediction && (
          <div className="mt-4 p-4 bg-gray-100 rounded-lg">
            <h3 className="font-bold">Results:</h3>
            <p>Prediction: {prediction}</p>
            {confidence && <p>Confidence: {confidence.toFixed(2)}%</p>}
          </div>
        )}
        
        {reportUrl && (
          <a 
            href={reportUrl}
            download
            className="block mt-4 text-center py-2 px-4 bg-green-600 text-white rounded-lg hover:bg-green-700"
          >
            Download Report
          </a>
        )}
      </div>
    </div>
  );
};

export default Upload;