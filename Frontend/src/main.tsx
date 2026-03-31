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
              const [complaints, clusters] = await Promise.all([
                fetch("/sample/complaints.json").then(res => res.json()),
                fetch("/sample/cluster.json").then(res => res.json())
              ])

              return {complaints, clusters}
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
