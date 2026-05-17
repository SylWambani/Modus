import React, { useState } from "react";
import { Box, Heading, Input, Button, Stack, Text } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";

const LogInPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    // TODO: Add authentication logic
    console.log("Login attempt:", { email, password });
  };

  return (
    <Box
      minH="100svh"
      display="flex"
      alignItems="center"
      justifyContent="center"
      bg="gray.50"
      _dark={{ bg: "gray.900" }}
    >
      <Box
        w="full"
        maxW="md"
        p={8}
        bg="white"
        _dark={{ bg: "gray.800" }}
        rounded="lg"
        boxShadow="md"
      >
        <Heading as="h1" size="lg" mb={6} textAlign="center">
          Sign In
        </Heading>

        <Stack gap={4}>
          <Box>
            <Text fontSize="sm" fontWeight="600" mb={2}>
              Email
            </Text>
            <Input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </Box>

          <Box>
            <Text fontSize="sm" fontWeight="600" mb={2}>
              Password
            </Text>
            <Input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </Box>

          <Button colorScheme="blue" onClick={handleLogin}>
            Sign In
          </Button>

          <Button variant="ghost" onClick={() => navigate("/")}>
            Back to Home
          </Button>
        </Stack>
      </Box>
    </Box>
  );
};

export default LogInPage;
