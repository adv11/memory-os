import { LoginButton } from "@/features/auth/LoginButton";

export default function HomePage() {
  return (
    <main className="min-h-screen">
      <section className="mx-auto grid min-h-screen max-w-6xl content-center gap-10 px-5 py-10 md:grid-cols-[1.1fr_0.9fr] md:items-center">
        <div>
          <p className="mb-3 text-sm font-semibold uppercase tracking-wide text-moss">
            MemoryOS
          </p>
          <h1 className="max-w-3xl text-5xl font-semibold leading-tight text-ink md:text-6xl">
            Remember what you learn.
          </h1>
          <p className="mt-5 max-w-2xl text-lg leading-8 text-ink/72">
            Capture topics, learning sessions, resources, and concepts in one
            structured system built for long-term learning.
          </p>
          <div className="mt-8">
            <LoginButton />
          </div>
        </div>

        <div className="border-l-4 border-moss bg-white p-6 shadow-soft">
          <div className="space-y-5">
            <div>
              <p className="text-sm font-semibold text-marine">Today</p>
              <h2 className="mt-1 text-2xl font-semibold text-ink">
                UML Diagrams
              </h2>
              <p className="mt-2 text-sm leading-6 text-ink/70">
                Class diagrams, sequence diagrams, activity diagrams.
              </p>
            </div>
            <div className="grid grid-cols-3 gap-3 text-sm">
              <div className="border border-line p-3">
                <p className="font-semibold text-ink">8/10</p>
                <p className="mt-1 text-ink/60">Difficulty</p>
              </div>
              <div className="border border-line p-3">
                <p className="font-semibold text-ink">4</p>
                <p className="mt-1 text-ink/60">Concepts</p>
              </div>
              <div className="border border-line p-3">
                <p className="font-semibold text-ink">3</p>
                <p className="mt-1 text-ink/60">Resources</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

