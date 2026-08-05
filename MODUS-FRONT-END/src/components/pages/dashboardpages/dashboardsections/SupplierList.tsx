import { Box, Heading, Spinner, Table, Text } from '@chakra-ui/react'
import { useEffect, useState } from 'react'
import { type Supplier, fetchSuppliers } from '../../../../api/suppliers';



const SupplierList = () => {
  const [suppliers, setSuppliers] = useState<Supplier[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadSuppliers = async () => {
      try {
        const data = await fetchSuppliers();
        setSuppliers(data);
      } catch (err: any) {
        setError("Failed to load suppliers");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    loadSuppliers();
  }, []);

  if (loading) return <Spinner />;
  if (error) return <Text color="red.500">{error}</Text>;
  return (
    <Box>
      <Heading size="md" mb={4}>Suppliers</Heading>
      <Table.Root>
        <Table.Header>
          <Table.Row>
            <Table.ColumnHeader>Name</Table.ColumnHeader>
            <Table.ColumnHeader>Email</Table.ColumnHeader>
            <Table.ColumnHeader>Phone</Table.ColumnHeader>
          </Table.Row>
        </Table.Header>
        <Table.Body>
          {suppliers.map((s) => (
            <Table.Row key={s.id}>
              <Table.Cell>{s.name}</Table.Cell>
              <Table.Cell>{s.email}</Table.Cell>
              <Table.Cell>{s.phone}</Table.Cell>
            </Table.Row>
          ))}
        </Table.Body>
      </Table.Root>
    </Box>
  )
}

export default SupplierList