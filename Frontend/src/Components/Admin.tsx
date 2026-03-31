import { Outlet, useNavigation } from "react-router-dom";
import { useState, useEffect } from 'react';

const DotLoader = () => {
  const [dots, setDots] = useState('.');
  
  useEffect(() => {
    const cycle = ['.', '..', '...', ''];
    let i = 0;
    
    const interval = setInterval(() => {
      i = (i + 1) % cycle.length;
      setDots(cycle[i]);
    }, 500);

    return () => clearInterval(interval);
  }, []);
  return <span className="inline-block w-8 text-left">{dots}</span>;
};

function Admin(){
    const navigation = useNavigation();
    const isLoading = navigation.state === "loading"

    if(isLoading){
        return <div className="flex flex-col flex-1">
            <div className="flex items-center h-full w-full justify-around text-4xl">
                <div>Generating Visualisation<DotLoader /></div>
            </div>
        </div>
    }

    return <div className="flex flex-col flex-1">
        <Outlet />
    </div>
}

export default Admin