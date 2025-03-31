import { MdOutlineFileDownload } from "react-icons/md";

const Report = () => {
  const handleDownload = () => {
    window.open("http://127.0.0.1:5000/download-report", "_blank");
  };

  return (
    <div className="w-screen flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <h1 className="text-3xl font-bold mb-4 text-center">Download Report</h1>
      <p className="mb-10 text-xl">Your report has been generated.</p>
      <div className="flex bg-[#1a1a1a] justify-center items-center px-4 py-2 rounded-xl gap-2 text-white hover:text-sky-400">
        <MdOutlineFileDownload className='text-2xl '/>
        <button
          onClick={handleDownload}
          className=""
        >
          Download
        </button>
      </div>
    </div>
  );
};

export default Report;
