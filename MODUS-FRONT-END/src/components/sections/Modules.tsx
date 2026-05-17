import {
  Box,
  Heading,
  SimpleGrid,
  Stack,
  Text,
  Button,
} from "@chakra-ui/react";

const moduleCards = [
  {
    icon: "📦",
    title: "Procurement",
    description: "Manage suppliers, quotations and purchase orders.",
  },
  {
    icon: "📦",
    title: "Inventory",
    description:
      "Track stock levels, product movement and warehouse workflows.",
  },
  {
    icon: "👥",
    title: "HR",
    description: "Handle employee records, attendance and role-based access.",
  },
  {
    icon: "📊",
    title: "Accounting",
    description: "Monitor invoices, expenses and financial performance.",
  },
];

const Modules = () => {
  return (
    <Box
      as="section"
      bg="gray.50"
      _dark={{ bg: "gray.900" }}
      py={12}
      px={{ base: 4, md: 8 }}
    >
      <Stack gap={6} maxW="7xl" mx="auto">
        <Box maxW="3xl">
          <Heading as="h2" size="xl" mb={3}>
            Modules
          </Heading>
          <Text fontSize="lg" color="gray.600" _dark={{ color: "gray.300" }}>
            Access your ERP mini apps from one place. Each module is built to
            help teams move faster, stay aligned and act with confidence.
          </Text>
        </Box>

        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} gap={6}>
          {moduleCards.map((module) => (
            <Box
              key={module.title}
              p={6}
              rounded="3xl"
              bg="white"
              border="1px solid"
              borderColor="gray.200"
              _dark={{ bg: "gray.800", borderColor: "gray.700" }}
              boxShadow="base"
              transition="transform 0.25s ease, box-shadow 0.25s ease"
              _hover={{ transform: "translateY(-8px)", boxShadow: "xl" }}
            >
              <Stack gap={4} h="full">
                <Text fontSize="3xl">{module.icon}</Text>
                <Heading as="h3" size="md">
                  {module.title}
                </Heading>
                <Text
                  color="gray.600"
                  _dark={{ color: "gray.400" }}
                  flexGrow={1}
                >
                  {module.description}
                </Text>
                <Button
                  size="sm"
                  colorScheme="blue"
                  alignSelf="start"
                  aria-label={`Enter ${module.title} module`}
                >
                  Enter Module
                </Button>
              </Stack>
            </Box>
          ))}
        </SimpleGrid>
      </Stack>
    </Box>
  );
};

export default Modules;
