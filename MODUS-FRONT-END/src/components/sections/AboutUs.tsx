import { Box, Heading, List, Text } from "@chakra-ui/react";
import { LuCircleCheck } from "react-icons/lu";

const AboutUs = () => {
  return (
    <Box>
      <Heading as="h2" size="xl" mb={4}>
        Built for Efficient Organizational Operations
      </Heading>
      <Text>
        MODUS ERP helps organizations streamline daily operations through
        centralized workflows, approval processes, audit tracking and real-time
        reporting across multiple departments.
      </Text>
      <List.Root mt={4}>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Centralized Operations: Access procurement, inventory, HR and
          accounting tools from one platform.
        </List.Item>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Audit trail: Track user activities and system changes for improved
          accountability.
        </List.Item>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Workflow Approvals: Simplify approval processes for requests,
          purchases and operational tasks.
        </List.Item>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Reporting and insights: Generate reports and monitor organizational
          performance in real time.
        </List.Item>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Role-Based Access: Control system access using secure user roles and
          permissions.
        </List.Item>
        <List.Item>
          <List.Indicator color="green.500">
            <LuCircleCheck />
          </List.Indicator>
          Data Security: Protect organizational information through secure
          authentication and access control.
        </List.Item>
      </List.Root>
    </Box>
  );
};

export default AboutUs;
