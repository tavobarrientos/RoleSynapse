import { useState } from "react";
import { LoginContext } from "../../loginContext";
import Layout from "./Layout";

const LayoutWrapper = () => {
    const [loggedIn, setLoggedIn] = useState(false);

    return (
        <LoginContext.Provider value={{ loggedIn, setLoggedIn }}>
            <Layout />
        </LoginContext.Provider>
    );
};

export default LayoutWrapper;