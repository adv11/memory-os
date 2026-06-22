import { apiBaseUrl } from "@/lib/config";

export type CurrentUser = {
  id: string;
  email: string;
  name: string;
};

export async function getCurrentUser(): Promise<CurrentUser | null> {
  const response = await fetch(`${apiBaseUrl}/api/v1/me`, {
    credentials: "include",
    cache: "no-store",
  });

  if (response.status === 401 || response.status === 403) {
    return null;
  }

  if (!response.ok) {
    throw new Error("Unable to load current user");
  }

  return response.json();
}

