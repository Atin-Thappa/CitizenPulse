import { Link } from "react-router-dom"

function NotFound(){
    return <div className="flex flex-col items-center justify-center h-full text-2xl gap-4">
        Error 404: Not Found <br />
        <Link to="/">Go Home!</Link>
    </div>
}

export default NotFound