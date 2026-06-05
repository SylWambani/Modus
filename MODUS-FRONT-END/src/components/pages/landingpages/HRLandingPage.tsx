import React from "react";
import {
  Container,
  Flex,
  Box,
  Heading,
  Text,
  Stack,
  List,
} from "@chakra-ui/react";
import Buttons from "../../sections/Buttons";
import Illustration from "../../sections/Illustration";
import { useNavigate } from "react-router-dom";

import { useColorModeValue } from "../../ui/color-mode";

const HRLandingPage: React.FC = () => {
  const navigate = useNavigate();
  const bg = useColorModeValue("gray.50", "gray.800");

  return (
    <Box bg={bg} minH="80vh" py={12}>
      <Container maxW="container.xl">
        <Flex direction={{ base: "column", md: "row" }} align="center" gap={12}>
          <Box flex="1">
            <Heading as="h1" size="2xl" mb={4}>
              HR, for people-first teams.
            </Heading>
            <Text fontSize="lg" color="gray.600" mb={6}>
              Manage employee records, attendance, and role-based access in a
              secure, compliant workflow.
            </Text>

            <Stack direction={{ base: "column", sm: "row" }} gap={4}>
              <Buttons
                onClick={() =>
                  navigate("/login", {
                    state: { redirectTo: "/dashboard/hr" },
                  })
                }
                colorScheme="blue"
              >
                Sign in to HR
              </Buttons>
              <Buttons onClick={() => navigate("/dashboard/hr")}>
                Explore Demo
              </Buttons>
            </Stack>

            <Stack gap={3} mt={8}>
              <Heading as="h3" size="md">
                Key features
              </Heading>
              <List.Root gap={2}>
                <List.Item>Employee directory and profiles</List.Item>
                <List.Item>Attendance and leave management</List.Item>
                <List.Item>Role-based permissions</List.Item>
                <List.Item>Onboarding workflows</List.Item>
              </List.Root>
            </Stack>
          </Box>

          <Box flex="1" textAlign="center">
            <Illustration />
          </Box>
        </Flex>
      </Container>
    </Box>
  );
};

export default HRLandingPage;
