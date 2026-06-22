"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { LoginButton } from "@/features/auth/LoginButton";
import { CurrentUser, getCurrentUser } from "@/lib/api";

export default function DashboardPage() {
  const [user, setUser] = useState<CurrentUser | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCurrentUser()
      .then(setUser)
      .catch(() => setError("Unable to load your account."))
      .finally(() => setIsLoading(false));
  }, []);

  if (isLoading) {
    return (
      <main className="mx-auto flex min-h-screen max-w-xl flex-col justify-center px-5">
        <p className="text-sm font-semibold uppercase tracking-wide text-moss">
          MemoryOS
        </p>
        <h1 className="mt-2 text-3xl font-semibold text-ink">
          Loading your workspace
        </h1>
      </main>
    );
  }

  if (!user) {
    return (
      <main className="mx-auto flex min-h-screen max-w-xl flex-col justify-center px-5">
        <h1 className="text-3xl font-semibold text-ink">Sign in required</h1>
        <p className="mt-3 leading-7 text-ink/70">
          {error ??
            "Your dashboard is tied to your Google account so your learning data stays scoped to you."}
        </p>
        <div className="mt-6">
          <LoginButton />
        </div>
      </main>
    );
  }

  return (
    <AppShell>
      <section className="flex flex-col gap-2">
        <p className="text-sm font-semibold uppercase tracking-wide text-moss">
          Dashboard
        </p>
        <h1 className="text-4xl font-semibold text-ink">Welcome, {user.name}</h1>
        <p className="max-w-2xl leading-7 text-ink/70">
          Phase 1 authentication is connected. Topic management will be the next
          product workflow added here.
        </p>
      </section>

      <section className="mt-8 grid gap-4 md:grid-cols-3">
        {[
          ["Topics", "0"],
          ["Learning Sessions", "0"],
          ["Concepts", "0"],
        ].map(([label, value]) => (
          <div key={label} className="border border-line bg-white p-5 shadow-soft">
            <p className="text-sm text-ink/60">{label}</p>
            <p className="mt-3 text-3xl font-semibold text-ink">{value}</p>
          </div>
        ))}
      </section>
    </AppShell>
  );
}
