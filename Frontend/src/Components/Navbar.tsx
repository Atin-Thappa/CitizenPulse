import { Link, /*useLocation*/} from "react-router-dom"
import { SlLogout } from "react-icons/sl"

function Navbar(){
    // const location = useLocation()
    // const isLoggedIn = location.pathname === "/admin/dashboard"

    return <nav className="bg-white shadow-xl flex items-center justify-between pl-4 pr-6">
        <div className="flex items-center font-bold cursor-default">
        <img src="../Logo.png" alt="Logo" />
        <span className="text-gray-900">Citizen</span><span className="text-slate-700">Pulse</span>
        </div>
        
        {/*isLoggedIn && */<Link to="/"><button className="bg-sky-700 px-2 rounded-lg text-white cursor-pointer hover:bg-sky-900 flex items-center gap-2"><SlLogout />Logout (decomment before shipping)</button></Link>}
    </nav>
}

export default Navbar