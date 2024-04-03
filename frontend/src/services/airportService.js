import API from "@/api/api";

export const fetchAirports = async () => {
  try {
    const response = await API.get('flights/airports/');
    return response.data;
  } catch (error) {
    console.error('Error fetch airport data:', error);
    throw error;
  }
};
