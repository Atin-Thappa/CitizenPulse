import { Outlet } from "react-router-dom"
import background from "./assets/Background.png"
import Navbar from "./Components/Navbar"
import Footer from "./Components/Footer"

function App(){
  return <div
  style={{backgroundImage: `url(${background})`}}
  className="h-screen bg-cover bg-center flex flex-col">
    <Navbar />
    <main className="flex-1 flex flex-col">
        <Outlet />
    </main>
    <Footer />
  </div>
}

export default App