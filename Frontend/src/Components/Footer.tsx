import { FaGithub } from "react-icons/fa"
function Footer(){
    return <footer className="flex items-center justify-between text-slate-500 bg-white py-1 px-5">
        <div></div>
        <p>
            &copy; 2026 Error:500 - ITS-A-HACK 2.0
        </p>
        <a href="#" className="cursor-pointer" target="_blank"><FaGithub /></a>
    </footer>
}

export default Footer