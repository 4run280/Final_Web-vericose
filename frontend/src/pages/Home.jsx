import Upload from "../components/Upload";
import { Link } from "react-router-dom";

const Home = () => {
  return (
    <div className="w-screen flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white">
      <h1 className="text-4xl font-extrabold mb-6 drop-shadow-lg">Varicose Vein Detection</h1>

      <div className="bg-white p-8 rounded-xl shadow-lg text-black w-96">
        <Upload />
      </div>

      <Link to="/report" className="mt-6 text-lg font-semibold underline hover:text-yellow-400 transition duration-300">
        Download Report
      </Link>
    </div>
  );
};

export default Home;
