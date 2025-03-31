const Report = () => {
    const handleDownload = () => {
      window.open("http://127.0.0.1:5000/download-report", "_blank");
    };
  
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
        <h1 className="text-3xl font-bold mb-4">Download Report</h1>
        <button
          onClick={handleDownload}
          className="bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-green-600 transition"
        >
          Download Report
        </button>
      </div>
    );
  };
  
  export default Report;
  