import { loginUrl } from "@/lib/config";

export function LoginButton() {
  return (
    <a
      href={loginUrl}
      className="inline-flex h-11 items-center justify-center rounded bg-ink px-5 text-sm font-semibold text-white shadow-soft hover:bg-ink/90"
    >
      Continue with Google
    </a>
  );
}

