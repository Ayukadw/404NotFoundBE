/* eslint-disable react/prop-types */
import LoginPage from "../../pages/Login";
import {useContext} from "react";
import {AuthContext} from "../../providers/AuthProvider";
import HamsterLoader from "../loaders/Hamster";

import MainLayout from "./Main";


const PrivateRoute = ({ component }) => {
  const { isLoggedIn, isLoadingScreen } = useContext(AuthContext);

  if (isLoggedIn && !isLoadingScreen) {
  return <MainLayout> {component} </MainLayout>;
  } else if (!isLoggedIn && !isLoadingScreen) {
    return <LoginPage />;
  }
  return <HamsterLoader />; // Show loader while checking auth status
  // Render the child component or outlet
};

export default PrivateRoute;
