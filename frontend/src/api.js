
const API_BASE_URL = '/api';

export async function analyzeRequest(text) {
  try {
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
      }),
    });

    if (!response.ok) {
      console.error('API error:', response.status, await response.text());

      return {
        success: false,
      };
    }

    const data = await response.json();

    return {
      success: true,
      data: data,
    };
  } catch (error) {
    console.error('API request failed:', error);

    return {
      success: false,
    };
  }
}
