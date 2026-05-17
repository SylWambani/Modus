import {
  Button,
  type ButtonProps as ChakraButtonProps,
} from "@chakra-ui/react";

interface ButtonProps extends ChakraButtonProps {
  children: string;
  //onclick: () => void;
}

const Buttons = ({ children }: ButtonProps) => {
  return <Button>{children}</Button>;
};

export default Buttons;
