export const apiBaseUrl =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8080";

export const loginUrl = `${apiBaseUrl}/login/oauth2/authorization/google`;
export const logoutUrl = `${apiBaseUrl}/logout`;

