import { useNavigate, useParams } from "react-router-dom";
import { Box, Heading, Text, Stack } from "@chakra-ui/react";
import Buttons from "../sections/Buttons";
import { isAuthenticated, userHasModuleAccess, getUserRoles } from "../../utils/auth";

const moduleTitles: Record<string, string> = {
  procurement: "Procurement",
  inventory: "Inventory",
  hr: "Human Resource",
  accounting: "Accounting",
};

const moduleDescriptions: Record<string, string> = {
  procurement:
    "Review purchase orders, supplier approvals and procurement analytics.",
  inventory:
    "Monitor stock levels, transfers and warehouse activity in real time.",
  hr: "Manage team information, attendance, and payroll workflows.",
  accounting:
    "Track invoices, expenses, and financial reports with confidence.",
};

const DashBoardPage = () => {
  const navigate = useNavigate();
  const { module } = useParams<{ module?: string }>();
  const title = module ? moduleTitles[module] ?? "Dashboard" : "Dashboard";
  const authenticated = isAuthenticated();
  const authorized = module ? userHasModuleAccess(module) : true;
  const userRoles = getUserRoles();

  const handleSignIn = () => {
    navigate("/login", {
      state: { redirectTo: module ? `/dashboard/${module}` : "/dashboard" },
    });
  };

  if (module && moduleTitles[module] && module === "procurement") {
    if (!authenticated) {
      return (
        <Box p={8} maxW="3xl" mx="auto">
          <Heading as="h1" size="2xl" mb={4}>
            Procurement Dashboard
          </Heading>
          <Text mb={4} fontSize="lg">
            You must sign in with a procurement account to view this dashboard.
          </Text>
          <Buttons colorScheme="blue" onClick={handleSignIn}>
            Sign In to Procurement
          </Buttons>
        </Box>
      );
    }

    if (!authorized) {
      return (
        <Box p={8} maxW="3xl" mx="auto">
          <Heading as="h1" size="2xl" mb={4}>
            Access Denied
          </Heading>
          <Text mb={4} fontSize="lg">
            Your account does not have procurement permissions. If you believe
            this is an error, sign in with a procurement officer account.
          </Text>
          <Stack direction={{ base: "column", sm: "row" }} gap={4}>
            <Buttons colorScheme="blue" onClick={handleSignIn}>
              Sign In with Another Account
            </Buttons>
            <Buttons variant="ghost" onClick={() => navigate("/")}>
              Back to Home
            </Buttons>
          </Stack>
          {userRoles.length > 0 && (
            <Text mt={4} color="gray.500">
              Current roles: {userRoles.join(", ")}
            </Text>
          )}
        </Box>
      );
    }
  }

  return (
    <Box p={8} maxW="5xl" mx="auto">
      <Heading as="h1" size="3xl" mb={4}>
        {title} Dashboard
      </Heading>
      {module && moduleTitles[module] ? (
        <>
          <Text fontSize="lg" mb={4}>
            {moduleDescriptions[module]}
          </Text>
          {module === "procurement" ? (
            <Stack gap={3}>
              <Text>
                Procurement officers can create purchase orders, approve vendor
                quotes, and manage supplier workflows from here.
              </Text>
              <Text>Authorized roles: procurement, procurement_officer.</Text>
            </Stack>
          ) : module === "inventory" ? (
            <Stack gap={3}>
              <Text>
                Inventory team members can track stock, run inventory counts,
                and manage warehouse movements.
              </Text>
              <Text>Authorized roles: inventory, inventory_manager.</Text>
            </Stack>
          ) : module === "hr" ? (
            <Stack gap={3}>
              <Text>
                HR users can manage employees, leaves, and role-based access
                workflows.
              </Text>
              <Text>Authorized roles: hr, hr_manager.</Text>
            </Stack>
          ) : module === "accounting" ? (
            <Stack gap={3}>
              <Text>
                Accounting team members can review invoices, expenses, and
                financial reports.
              </Text>
              <Text>Authorized roles: accounting, finance.</Text>
            </Stack>
          ) : null}
        </>
      ) : (
        <Text fontSize="lg">
          Welcome to your main dashboard. Select a module to continue.
        </Text>
      )}
      {authenticated && userRoles.length > 0 && (
        <Text mt={6} color="gray.600">
          Signed in roles: {userRoles.join(", ")}
        </Text>
      )}
    </Box>
  );
};

export default DashBoardPage;
