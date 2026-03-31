import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import LandingPage from './Components/LandingPage.tsx'
import CitizenForm from './Components/CitizenForm.tsx'
import AdminDashboard from './Components/AdminDashboard.tsx'
import LoginForm from './Components/LoginForm.tsx'
import Admin from './Components/Admin.tsx'
import NotFound from './Components/NotFound.tsx'

const artificialStall = (ms = 1500) => new Promise(resolve => setTimeout(resolve, ms));

const router = createBrowserRouter([{
    path: "/",
    element: <App />,
    children: [
      {index: true, element: <LandingPage />},
      {path: "complaintform", element: <CitizenForm />},
      {
        path: "admin/",
        element: <Admin />,
        children:[
          {index: true, element: <LoginForm />},
          {
            path: "dashboard",
            element: <AdminDashboard />,
            loader: async () =>{
              await artificialStall(1500)
              const [clusters, heatmap] = await Promise.all([
                fetch("http://localhost:8000/clusters", { credentials: "include" }).then(r => r.json()),
                fetch("http://localhost:8000/heatmap", { credentials: "include" }).then(r => r.json()),
              ])
              return {clusters, heatmap}
            } 
          }
        ]
      }
    ]
  },
  {path: "*", element: <NotFound />}
])

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>
)
