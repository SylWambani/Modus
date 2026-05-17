import {
  Button,
  type ButtonProps as ChakraButtonProps,
} from "@chakra-ui/react";

interface ButtonProps extends ChakraButtonProps {
  children: string;
}

const Buttons = ({ children, ...props }: ButtonProps) => {
  return <Button {...props}>{children}</Button>;
};

export default Buttons;
