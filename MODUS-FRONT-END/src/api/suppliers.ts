import axiosInstance from "./axiosInstance";

export interface Supplier {
  id: number;
  name: string;
  email: string;
  phone: string;
}

export const fetchSuppliers = async (): Promise<Supplier[]> => {
  const res = await axiosInstance.get("/procurement/suppliers/");
  return res.data;
};