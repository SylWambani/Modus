import { useNavigate, useParams } from "react-router-dom";
import { Box, Heading, Text, Badge, VStack, HStack } from "@chakra-ui/react";
import Buttons from "../sections/Buttons";
import { useAuth } from "../../contexts/AuthContext";
import ProtectedSection from "../ui/ProtectedSection";

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
  const { user, logout } = useAuth();

  const title = module ? (moduleTitles[module] ?? "Dashboard") : "Dashboard";
  const authenticated = !!user;
  const userPermissions = user?.permissions || [];

  const handleSignIn = () => {
    navigate(`/${module}/login`);
  };

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  if (!authenticated) {
    return (
      <Box p={8} maxW="3xl" mx="auto">
        <Heading as="h1" size="2xl" mb={4}>
          {title} Dashboard
        </Heading>
        <Text mb={4} fontSize="lg">
          You must sign in to access this dashboard.
        </Text>
        <Buttons colorScheme="blue" onClick={handleSignIn}>
          Sign In
        </Buttons>
      </Box>
    );
  }

  return (
    <Box p={8} maxW="5xl" mx="auto">
      <HStack justify="space-between" mb={8}>
        <VStack align="start" gap={1}>
          <Heading as="h1" size="3xl">
            {title} Dashboard
          </Heading>
          <Text color="gray.600">
            Welcome, {user?.first_name || user?.username}
          </Text>
        </VStack>
        <Buttons colorScheme="red" size="sm" onClick={handleLogout}>
          Logout
        </Buttons>
      </HStack>

      {module && moduleTitles[module] ? (
        <>
          <Text fontSize="lg" mb={6}>
            {moduleDescriptions[module]}
          </Text>

          {/* User Info Section */}
          <Box
            bg="blue.50"
            p={4}
            borderRadius="md"
            mb={8}
            borderLeft="4px solid"
            borderColor="blue.400"
          >
            <Text fontWeight="bold" mb={2}>
              Your Permissions in this Module:
            </Text>
            {userPermissions.length > 0 ? (
              <HStack wrap="wrap" gap={2}>
                {userPermissions.map((perm) => (
                  <Badge key={perm} colorScheme="blue">
                    {perm}
                  </Badge>
                ))}
              </HStack>
            ) : (
              <Text color="gray.600">No specific permissions assigned.</Text>
            )}
          </Box>

          {/* Protected Sections based on module */}
          {module === "procurement" && (
            <VStack align="start" gap={6}>
              <ProtectedSection
                requiredPermissions={[
                  "add_purchaseorder",
                  "view_purchaseorder",
                ]}
                requireAny={true}
              >
                <Box
                  p={6}
                  borderRadius="lg"
                  border="1px solid"
                  borderColor="gray.200"
                >
                  <Heading as="h3" size="lg" mb={2}>
                    📋 Purchase Orders
                  </Heading>
                  <Text mb={4} color="gray.600">
                    Create, view, and manage purchase orders.
                  </Text>
                  <Buttons colorScheme="green" size="sm">
                    View Purchase Orders
                  </Buttons>
                </Box>
              </ProtectedSection>

              <ProtectedSection
                requiredPermissions={["add_supplier", "view_supplier"]}
                requireAny={true}
              >
                <Box
                  p={6}
                  borderRadius="lg"
                  border="1px solid"
                  borderColor="gray.200"
                >
                  <Heading as="h3" size="lg" mb={2}>
                    🏢 Suppliers
                  </Heading>
                  <Text mb={4} color="gray.600">
                    Manage suppliers and vendor information.
                  </Text>
                  <Buttons colorScheme="green" size="sm">
                    View Suppliers
                  </Buttons>
                </Box>
              </ProtectedSection>

              <ProtectedSection requiredPermissions={["view_approval"]}>
                <Box
                  p={6}
                  borderRadius="lg"
                  border="1px solid"
                  borderColor="gray.200"
                >
                  <Heading as="h3" size="lg" mb={2}>
                    ✅ Approvals
                  </Heading>
                  <Text mb={4} color="gray.600">
                    Review and approve pending procurement requests.
                  </Text>
                  <Buttons colorScheme="green" size="sm">
                    View Pending Approvals
                  </Buttons>
                </Box>
              </ProtectedSection>
            </VStack>
          )}

          {module === "inventory" && (
            <VStack align="start" gap={6}>
              <ProtectedSection requiredPermissions={["view_product"]}>
                <Box
                  p={6}
                  borderRadius="lg"
                  border="1px solid"
                  borderColor="gray.200"
                >
                  <Heading as="h3" size="lg" mb={2}>
                    📦 Products
                  </Heading>
                  <Text mb={4} color="gray.600">
                    View and manage product inventory.
                  </Text>
                  <Buttons colorScheme="green" size="sm">
                    View Products
                  </Buttons>
                </Box>
              </ProtectedSection>
            </VStack>
          )}
        </>
      ) : (
        <Text fontSize="lg">
          Welcome to your main dashboard. Select a module to continue.
        </Text>
      )}
    </Box>
  );
};

export default DashBoardPage;
