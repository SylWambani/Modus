import { Container } from "@chakra-ui/react"
import HeroSection from "../sections/HeroSection"
import AboutUs from "../sections/AboutUs"
import Modules from "../sections/Modules"


const HomePage = () => {
  return (
    <Container fluid >
      <HeroSection />
      <Modules/>
      <AboutUs/>

    </Container>
    
  )
}

export default HomePage