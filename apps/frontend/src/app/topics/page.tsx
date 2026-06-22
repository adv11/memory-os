import { AppShell } from "@/components/AppShell";

export default function TopicsPage() {
  return (
    <AppShell>
      <section>
        <p className="text-sm font-semibold uppercase tracking-wide text-moss">
          Topics
        </p>
        <h1 className="mt-2 text-4xl font-semibold text-ink">Learning Areas</h1>
        <p className="mt-3 max-w-2xl leading-7 text-ink/70">
          Topic management starts in Phase 2. This route exists so the product
          shell can grow without reshaping navigation later.
        </p>
      </section>
    </AppShell>
  );
}

