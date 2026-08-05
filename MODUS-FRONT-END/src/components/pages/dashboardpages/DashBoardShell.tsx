import React from "react";
import { Box } from "@chakra-ui/react";
import WelcomeBanner from "./WelcomeBanner";

interface DashboardShellProps {
  children: React.ReactNode;
}

const DashBoardShell: React.FC<DashboardShellProps> = ({ children }) => {
  return (
    <Box p={6}>
      <WelcomeBanner />
      {children}
    </Box>
  );
};

export default DashBoardShell;



