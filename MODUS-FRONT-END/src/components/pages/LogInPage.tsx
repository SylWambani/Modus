import React, { useState } from "react";
import { Box, Heading, Input, Button, Stack, Text } from "@chakra-ui/react";
import { useNavigate } from "react-router-dom";
import Buttons from "../sections/Buttons"

const LogInPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogIn = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    if (!email && !password) {
      setError("Username and password are required");
      return;
    }

    if (!email) {
      setError("Username is required");
      return;
    }

    if (!password) {
      setError("Password is required");
      return;
    }

    setError("");
    /*Nexttime use axiosInstance tp fetch*/
    try {
      setLoading(true);
      const res = await fetch("http://127.0.0.1:8000/auth/jwt/create/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await res.json();

      if (!res.ok) {
        if (res.status === 400 || res.status === 401) {
          throw new Error("Invalid username or password");
        }

        if (res.status >= 500) {
          throw new Error("Server error. Please try again later.");
        }

        throw new Error("Something went wrong. Please try again.");
      }

      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);
      localStorage.setItem("loginSuccess", "true");
      navigate("/dashboard");
    } catch (error: any) {
      setError(error.message);
      console.error(error);
    } finally {
      setLoading(false);
    }
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

          <Buttons colorScheme="blue" onClick={handleLogIn}>
            Sign In
          </Buttons>

          <Buttons variant="ghost" onClick={() => navigate("/")}>
            Back to Home
          </Buttons>
        </Stack>
      </Box>
    </Box>
  );
};

export default LogInPage;
