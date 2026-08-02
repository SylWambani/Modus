import React from "react";
import { Box, Heading, Text, Stack } from "@chakra-ui/react";
import { useAuth } from "../../contexts/AuthContext";
import Buttons from "../sections/Buttons";

interface ProtectedRouteProps {
  requiredModule?: string;
  children: React.ReactNode;
}

/**
 * ProtectedRoute - Guards routes and ensures user is authenticated and has module access
 * @param requiredModule - Module the route belongs to (e.g., "procurement", "inventory")
 * @param children - Component to render if authorized
 */
export const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  requiredModule,
  children,
}) => {
  const { user } = useAuth();

  // Not authenticated
  if (!user) {
    return (
      <Box p={8} maxW="3xl" mx="auto" textAlign="center">
        <Heading as="h1" size="2xl" mb={4}>
          Authentication Required
        </Heading>
        <Text mb={6} fontSize="lg" color="gray.600">
          You must be logged in to access this page.
        </Text>
        <Buttons
          colorScheme="blue"
          onClick={() => {
            if (requiredModule) {
              window.location.href = `/${requiredModule}/login`;
            } else {
              window.location.href = "/";
            }
          }}
        >
          Go to Login
        </Buttons>
      </Box>
    );
  }

  // Check module access
  if (requiredModule && !user.modules?.includes(requiredModule)) {
    return (
      <Box p={8} maxW="3xl" mx="auto" textAlign="center">
        <Heading as="h1" size="2xl" mb={4} color="red.600">
          Access Denied
        </Heading>
        <Text mb={4} fontSize="lg" color="gray.600">
          Your account does not have access to the{" "}
          <strong>{requiredModule}</strong> module.
        </Text>
        <Text mb={6} color="gray.500">
          You have access to:{" "}
          {user.modules?.length ? user.modules.join(", ") : "no modules"}
        </Text>
        <Stack
          direction={{ base: "column", sm: "row" }}
          gap={4}
          justify="center"
        >
          <Buttons
            colorScheme="blue"
            onClick={() => {
              window.location.href = "/";
            }}
          >
            Back to Home
          </Buttons>
        </Stack>
      </Box>
    );
  }

  return <>{children}</>;
};

export default ProtectedRoute;
