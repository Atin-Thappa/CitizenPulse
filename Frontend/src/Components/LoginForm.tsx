import { useForm } from "react-hook-form"
import { useNavigate } from "react-router-dom";
import api from "../api/client";

interface FormData{
    email: string
    password: string
}

function LoginForm(){
    const {register, handleSubmit,formState:{errors}, setError} = useForm<FormData>()
    const navigate = useNavigate()


   async function onSubmit(data: FormData):Promise<void>{
       const result = await api.login(data.email, data.password)
       if (result.status === "success") {
           navigate("/admin/dashboard")
        } else {
            setError("root", { message: result.detail || "Wrong Credentials" })
        }
    }

    function handleCancel():void{
        navigate("/")
    }


    return <div
    className="flex flex-col items-center justify-center text-center flex-1 gap-6 py-8 overflow-y-auto">
        <h1 className="text-5xl font-bold text-center">Government Portal Login</h1>
        <form onSubmit={handleSubmit(onSubmit)} className="min-h-1/2 w-11/12 sm:w-2/3 md:w-1/2 lg:w-1/3 h-fit">
            <div className="flex flex-col items-center px-4 py-2 gap-2 h-full w-full justify-around text-lg ring-2 ring-neutral-400 shadow-2xl rounded-lg bg-white">
                <label htmlFor="form" className="text-3xl font-semibold text-blue-800">Government Portal Login</label>
                <input
                type="text"
                id="email"
                {...register("email", {
                    required: "Please  provide your Email ID",
                    pattern: {
                        value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i,
                        message: 'Invalid email address'
                    }              
                })}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1"
                placeholder="[Your Email ID]"
                />
                {errors.email && <p className="text-red-500">{errors.email.message}</p>}
                <input
                type="password"
                id="password"
                {...register("password", {required: "Enter Password"})}
                className="ring-2 ring-gray-400 w-full rounded-lg text-center p-1"
                placeholder="[Password]"
                />
                {errors.password && <p className="text-red-500">{errors.password.message}</p>}
                {errors.root && (
                    <p className="text-red-500 font-bold animate-bounce">
                    {errors.root.message}
                    </p>
                )}
                <div className="flex w-full justify-around">
                <button
                type="submit"
                className="cursor-pointer flex-1 flex items-center justify-center text-white bg-fuchsia-900 py-2 rounded-full ring-fuchsia-950"
                >Login</button>
                <button
                type="button"
                onClick={handleCancel}
                className="cursor-pointer flex-1 flex items-center justify-center ring-2 ring-fuchsia-900 text-fuchsia-900 py-2 rounded-full shadow-lg"
                >Cancel</button>
                </div>
            </div>
        </form>
    </div>
}

export default LoginForm