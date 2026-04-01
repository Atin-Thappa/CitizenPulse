import { useForm } from "react-hook-form"
import toast, { Toaster } from "react-hot-toast"
import { useNavigate } from "react-router-dom"
import { DISTRICT_OPTIONS } from "../constants/districts"
import api from "../api/client"

interface FormData{
    name: string
    email: string
    description: string
    category: string
    location: string
}

function CitizenForm(){
    const {register, handleSubmit,formState:{errors}} = useForm<FormData>()
    const navigate = useNavigate()

    async function onSubmit(data: FormData): Promise<void> {
  const result = await api.submitComplaint({
    citizen_name: data.name,
    citizen_email: data.email,
    raw_text: data.description,
    category: data.category,
    district: data.location,
  })
  if (result.complaint_id) {
    toast.success("Success! Report Submitted.", {
            position: "top-right",
            duration: 2500,
            style:{
                border: "1px solid gray",
                padding: "16px",
                color: "black"
            }
        })
    setTimeout(() => navigate("/"), 2750)
  } else {
    toast.error(result.detail || result.error || "Submission failed.")
  }
}

    function handleCancel():void{
        navigate("/")
    }


    return <div
    className="flex flex-col items-center justify-center text-center flex-1 gap-6 py-8 overflow-y-auto">
        <Toaster />

        <h1 className="text-5xl font-bold text-center">File a Community Complaint</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="h-3/5 w-11/12 sm:w-2/3 md:w-1/2 lg:w-1/3 h-fit">
            <div className="flex flex-col items-center px-4 py-2 gap-2 h-full w-full justify-around text-lg rounded-lg bg-white ring-2 ring-neutral-400 shadow-2xl ">
                <label htmlFor="form" className="text-3xl font-semibold text-blue-800">File a Community Complaint</label>
                <input
                type="text"
                id="name"
                {...register("name",{
                    required: "Please enter your name"
                })}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1"
                placeholder="[Full Name]"
                />
                {errors.name && <p className="text-red-500">{errors.name.message}</p>}
                <input
                type="text"
                id="email"
                {...register("email", {
                    required: "Please provide your Email ID",
                    pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                    }              
                })}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1"
                placeholder="[Your Email ID]"
                />
                {errors.email && <p className="text-red-500">{errors.email.message}</p>}
                <select
                {...register("location", { required: "Please select a district" })}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1">
                    <option value="">Select District</option>
                    {DISTRICT_OPTIONS.map((d) => (
                        <option key={d} value={d}>{d}</option>
                    ))}
                </select>
                {errors.location && <p className="text-red-500">{errors.location.message}</p>}
                <select
                {...register("category", {required: "Please select a category"})}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1">
                    <option value="">Select Category</option>
                    {["Infrastructure", "Public Safety", "Sanitation", "Water Supply", "Traffic", "Maintenance", "Emergency"].map(c =>(
                        <option key={c} value={c}>{c}</option>
                    ))}
                </select>

                <textarea
                id="description"
                {...register("description", {
                    required: "Please provide a description of the issue"
                })}
                className="ring-2 ring-gray-400 w-full rounded-lg p-1 h-2/1"
                placeholder="[Description of the issue]"
                />
                {errors.description && <p className="text-red-500">{errors.description.message}</p>}
                <button
                type="submit"
                className="cursor-pointer mx-8 flex items-center text-white bg-fuchsia-900 py-2 px-4 rounded-full ring-fuchsia-950 w-full justify-center"
                >Submit Report</button>
                <button
                type="button"
                onClick={handleCancel}
                className="cursor-pointer mx-8 flex items-center ring-2 ring-fuchsia-900 text-fuchsia-900 px-4 py-2 rounded-full shadow-lg w-full justify-center"
                >Cancel</button>
            </div>
        </form>
    </div>
}

export default CitizenForm