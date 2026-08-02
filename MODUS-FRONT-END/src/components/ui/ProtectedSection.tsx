import React from "react";
import { Box, Text } from "@chakra-ui/react";
import { useAuth } from "../../contexts/AuthContext";

interface ProtectedSectionProps {
  requiredPermissions?: string[];
  requireAny?: boolean;
  fallback?: React.ReactNode;
  children: React.ReactNode;
}

/**
 * ProtectedSection - Renders children only if user has the required permissions
 * @param requiredPermissions - Array of permissions required (defaults to all required)
 * @param requireAny - If true, user needs ANY of the permissions; if false (default), needs ALL
 * @param fallback - Component to show if user lacks permissions
 * @param children - Content to render if authorized
 */
export const ProtectedSection: React.FC<ProtectedSectionProps> = ({
  requiredPermissions = [],
  requireAny = false,
  fallback,
  children,
}) => {
  const { user } = useAuth();

  if (!requiredPermissions || requiredPermissions.length === 0) {
    return <>{children}</>;
  }

  const userPermissions = user?.permissions || [];

  const hasPermission = requireAny
    ? requiredPermissions.some((perm) => userPermissions.includes(perm))
    : requiredPermissions.every((perm) => userPermissions.includes(perm));

  if (!hasPermission) {
    return (
      fallback || (
        <Box
          p={4}
          border="1px solid"
          borderColor="orange.200"
          borderRadius="md"
          bg="orange.50"
        >
          <Text color="orange.800">
            You do not have permission to access this section.
          </Text>
        </Box>
      )
    );
  }

  return <>{children}</>;
};

export default ProtectedSection;
