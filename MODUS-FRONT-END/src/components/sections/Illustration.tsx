import { Image } from "@chakra-ui/react";
import pic from "../../assets/undraw_web-app_141a.svg";

const Illustration = () => {
  return (
    <Image
      src={pic}
      alt="Dashboard Illustration"
      fit="contain"
      htmlWidth="400px"
      htmlHeight="400px"
    />
  );
};

export default Illustration;
