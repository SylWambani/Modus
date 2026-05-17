import { Box } from "@chakra-ui/react";
import { Outlet } from "react-router-dom";
import NavBarSection from "../sections/NavBarSection";
import Logo from "../sections/Logo";
import FooterSection from "../sections/FooterSection";

const HomePageLayout = () => {
  return (
    <Box display="flex" minH="100svh" flexDirection="column" >
      <NavBarSection>
        <Logo />
      </NavBarSection>

      {/* Page content */}
      <Box flex="1">
        <Outlet />
      </Box>
      <FooterSection />
    </Box>
  );
};

export default HomePageLayout;
