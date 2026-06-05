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

const AccountingLandingPage: React.FC = () => {
  const navigate = useNavigate();
  const bg = useColorModeValue("gray.50", "gray.800");

  return (
    <Box bg={bg} minH="80vh" py={12}>
      <Container maxW="container.xl">
        <Flex direction={{ base: "column", md: "row" }} align="center" gap={12}>
          <Box flex="1">
            <Heading as="h1" size="2xl" mb={4}>
              Accounting, simplified.
            </Heading>
            <Text fontSize="lg" color="gray.600" mb={6}>
              Monitor invoices, expenses and financial performance with clear
              reporting and reconciliation tools.
            </Text>

            <Stack direction={{ base: "column", sm: "row" }} gap={4}>
              <Buttons
                onClick={() =>
                  navigate("/login", {
                    state: { redirectTo: "/dashboard/accounting" },
                  })
                }
                colorScheme="blue"
              >
                Sign in to Accounting
              </Buttons>
              <Buttons onClick={() => navigate("/dashboard/accounting")}>
                Explore Demo
              </Buttons>
            </Stack>

            <Stack gap={3} mt={8}>
              <Heading as="h3" size="md">
                Key features
              </Heading>
              <List.Root gap={2}>
                <List.Item>Invoice and expense tracking</List.Item>
                <List.Item>Financial reports and dashboards</List.Item>
                <List.Item>Multi-currency support</List.Item>
                <List.Item>Reconciliation tools</List.Item>
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

export default AccountingLandingPage;
