import React, { useState } from "react";
import { Box, Heading, Input, Stack, Text } from "@chakra-ui/react";
import { useNavigate, useLocation } from "react-router-dom";
import Buttons from "../sections/Buttons";
import { decodeJwtPayload } from "../../utils/auth";

interface LoginLocationState {
  redirectTo?: string;
}

const LogInPage = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();
  const selectedModule = (location.state as LoginLocationState)?.module;

  // const locationState = location.state as LoginLocationState | null;
  // const redirectTo = locationState?.redirectTo ?? "/dashboard";

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
    if (!selectedModule) {
      setError("No module selected. Please choose a module first.");
      navigate("/");
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

      const meRes = await fetch(
  "http://127.0.0.1:8000/auth/me/",
  {
    method: "GET",
    headers: {
      Authorization: `Bearer ${data.access}`,
      "Content-Type": "application/json",
    },
  }
);

if (!meRes.ok) {
        throw new Error("Failed to load user profile");
      }

const meData = await meRes.json();

 localStorage.setItem("userEmail", meData.email);
      localStorage.setItem(
        "userModules",
        JSON.stringify(meData.modules)
      );
      localStorage.setItem("currentModule", selectedModule);



if (
  meData.modules.includes(selectedModule)
) {
  navigate(`/${selectedModule}/dashboard`);
} else if (!selectedModule) {
  setError("No module selected.");
  navigate("/");
  return;
}
else {
  setError(
    "You do not have permission to access this module."
  );
}
      // const claims = decodeJwtPayload(data.access);
      // const roles = Array.isArray(claims?.roles)
      //   ? claims.roles
      //   : claims?.role
      //     ? String(claims.role).split(/[,\s]+/)
      //     : [];

      // if (roles.length) {
      //   localStorage.setItem(
      //     "userRoles",
      //     JSON.stringify(roles.map((role) => String(role).toLowerCase())),
      //   );
      // }

      // if (claims?.email) {
      //   localStorage.setItem("userEmail", String(claims.email));
      // }

//       const redirectUser = (modules: string[]) => {
//   if (modules.length === 1) {
//     navigate(`/${modules[0]}/dashboard`);
//     return;
//   }

//   navigate("/workspace");
// };
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
        {error && (
          <Text color="red.500" textAlign="center" mb={4}>
            {error}
          </Text>
        )}

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

          <Buttons
            colorScheme="blue"
            onClick={handleLogIn}
            loading={loading}
            loadingText="Signing in..."
            disabled={loading}
          >
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
