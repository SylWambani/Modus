import { Box, Text } from "@chakra-ui/react";
import Buttons from "./Buttons";
import Illustration from "./Illustration";

const HeroSection = () => {
  return (
    <Box>
      <Text>Smart ERP Solutions for Modern Organizations</Text>
      <Text>
        Monitor operations, manage departments and streamline daily workflows
        through one integrated ERP platform.
      </Text>
      <Buttons>Explore Modules</Buttons>
      <Illustration />
    </Box>
  );
};

export default HeroSection;
