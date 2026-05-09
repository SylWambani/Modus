import { Container, HStack } from "@chakra-ui/react";

interface NavBarProps {
  children?: React.ReactNode;
}

const navbar = ({ children }: NavBarProps) => {
  return;
  <Container>
    <HStack
      display="flex"
      justifyContent="space-between"
      padding="8px"
      width="100%"
      backgroundColor="#1E3A8A"
    >
      {children}
    </HStack>
  </Container>;
};

export default navbar;
