import React from "react";
import { Badge, Box, Heading, Text } from "@chakra-ui/react";
import { useAuth } from "../../../contexts/AuthContext";

const getGreeting = () => {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
};
const WelcomeBanner: React.FC = () => {
  const { user, currentModule } = useAuth();

  const displayName =
    user?.first_name && user?.last_name
      ? `${user.first_name} ${user.last_name}`
      : user?.username || user?.email || "there";

  return (
    <Box mb={6}>
      <Box display="flex" alignItems="center" gap={3} flexWrap="wrap">
        <Heading as="h2" size="lg">
          {getGreeting()}, {displayName} 👋
        </Heading>
        {currentModule && (
          <Badge
            colorScheme="blue"
            fontSize="0.8em"
            px={2}
            py={1}
            borderRadius="md"
          >
            {currentModule.toUpperCase()}
          </Badge>
        )}
      </Box>
      <Text color="gray.500" mt={1}>
        Here's what's happening today.
      </Text>
    </Box>
  );
};

export default WelcomeBanner;
