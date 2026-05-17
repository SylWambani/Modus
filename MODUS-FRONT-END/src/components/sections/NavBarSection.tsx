import { Container, HStack } from "@chakra-ui/react";

interface NavBarProps {
  children?: React.ReactNode;
}

const NavBarSection = ({ children }: NavBarProps) => {
  return(
  <Container padding='0'>
    <HStack
      display="flex"
      justifyContent="space-between"
      padding="10px"
      width="100%"
      backgroundColor="#1E3A8A"
    >
      {children}
    </HStack>
  </Container>)
};

export default NavBarSection;
