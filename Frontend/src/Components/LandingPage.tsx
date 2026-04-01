import flowchart from "../assets/Flowchart.png"
import { FaLock } from "react-icons/fa"
import { IoMdMegaphone } from "react-icons/io"
import { useNavigate } from "react-router-dom"
function LandingPage(){
    const navigate = useNavigate()

    function handleLogin():void{        
        navigate("/admin")
    }

    function handleComplaint():void{
        navigate("/complaintform")
    }

    return <div
    className="flex flex-col items-center text-center gap-6 py-6">
        <div>
        <h1 className="font-bold text-4xl">
            Intelligent Infrastructure<br />
            Management
            </h1>
        <p className="font-medium text-md">
            Your City's AI-Powered Dashboard for Smarter Goverence.<br />
            Detect,clusters, and prioritizes multiple streams of community complaints - Automatically.
        </p>
        </div>
        <img
        src={`${flowchart}`}
        alt="flowchart"
        className="max-h-64 md:max-h-96 w-auto object-contain"
        />
        <div className="flex flex-col sm:flex-row items-center gap-4">
        <button
        className="cursor-pointer mx-8 flex items-center text-white bg-fuchsia-900 p-2 pr-4 rounded-full shadow-xl"
        onClick={handleLogin}
        ><FaLock className="mx-2"/>Government Portal Login</button>
        <button
        className="cursor-pointer mx-8 flex items-center ring-2 ring-fuchsia-900 text-fuchsia-900 p-2 pr-4 rounded-full shadow-lg"
        onClick={handleComplaint}
        ><IoMdMegaphone className="mx-2 text-2xl"/>File a Community Complaint</button>
        </div>
    </div>
}

export default LandingPage
