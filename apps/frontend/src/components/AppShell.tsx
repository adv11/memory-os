import Link from "next/link";
import { logoutUrl } from "@/lib/config";

type AppShellProps = {
  children: React.ReactNode;
};

const navItems = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/topics", label: "Topics" },
];

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-line bg-paper/90">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4">
          <Link href="/dashboard" className="text-lg font-semibold text-ink">
            MemoryOS
          </Link>
          <nav className="flex items-center gap-1 text-sm text-ink/75">
            {navItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded px-3 py-2 hover:bg-ink/5"
              >
                {item.label}
              </Link>
            ))}
            <a className="rounded px-3 py-2 hover:bg-ink/5" href={logoutUrl}>
              Logout
            </a>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-5 py-8">{children}</main>
    </div>
  );
}

