export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || '/api';

export async function fetchMarketData() {
    const response = await fetch(`${API_BASE_URL}/market`);
    return response.json();
}
