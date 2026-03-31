import { Link } from "react-router-dom"

function NotFound(){
    return <div>
        Error 404: Not Found <br />
        <Link to="/">Go Home!</Link>
    </div>
}

export default NotFound