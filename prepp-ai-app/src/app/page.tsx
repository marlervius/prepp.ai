"use client";

import { useState, useRef } from "react";
import { motion } from "framer-motion";
import {
  Sparkles,
  BookOpenCheck,
  ShieldCheck,
  Zap,
} from "lucide-react";
import Header from "@/components/Header";
import BriefForm from "@/components/BriefForm";
import BriefDisplay from "@/components/BriefDisplay";
import LoadingSkeleton from "@/components/LoadingSkeleton";
import type { Brief } from "@/types/brief";

const SELLING_POINTS = [
  { icon: ShieldCheck, label: "Kvalitetssikret mot LK20" },
  { icon: BookOpenCheck, label: "Kildebelagte referanser" },
  { icon: Zap, label: "Klar på sekunder" },
];

export default function Home() {
  const [currentBrief, setCurrentBrief] = useState<Brief | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const resultRef = useRef<HTMLDivElement>(null);

  const handleBriefGenerated = (brief: Brief) => {
    setCurrentBrief(brief);
    setIsLoading(false);
    // Scroll to results on mobile
    setTimeout(() => {
      resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
    }, 100);
  };

  const handleLoadingChange = (loading: boolean) => {
    setIsLoading(loading);
    if (loading) {
      setTimeout(() => {
        resultRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      }, 100);
    }
  };

  return (
    <div className="min-h-screen bg-[var(--color-surface-sunken)]">
      <Header />

      <main className="mx-auto max-w-6xl px-4 sm:px-6 py-6 sm:py-10">
        {/* Hero */}
        <motion.section
          initial={{ opacity: 0, y: 16 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-center mb-8 sm:mb-12"
        >
          <div className="inline-flex items-center gap-1.5 rounded-full border border-[var(--color-brand-200)] bg-[var(--color-brand-50)] px-3.5 py-1.5 text-xs font-medium text-[var(--color-brand-700)] mb-4">
            <Sparkles size={14} />
            AI-drevet lærerstøtte
          </div>

          <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-[var(--color-text-primary)] mb-3">
            Undervisningsbriefer{" "}
            <span className="gradient-text">på sekunder</span>
          </h1>

          <p className="text-base sm:text-lg text-[var(--color-text-secondary)] max-w-xl mx-auto mb-6">
            Kvalitetssikrede lærermanualer koblet til LK20, med kilder fra
            SNL, NDLA og Udir.
          </p>

          {/* Trust badges */}
          <div className="flex flex-wrap items-center justify-center gap-4 sm:gap-6">
            {SELLING_POINTS.map(({ icon: Icon, label }) => (
              <div
                key={label}
                className="flex items-center gap-1.5 text-xs sm:text-sm text-[var(--color-text-muted)]"
              >
                <Icon size={16} className="text-[var(--color-brand-500)]" />
                {label}
              </div>
            ))}
          </div>
        </motion.section>

        {/* Two-column / stacked layout */}
        <div className="grid gap-6 lg:grid-cols-[minmax(0,420px)_1fr] lg:items-start">
          {/* Form column */}
          <motion.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.1 }}
            className="lg:sticky lg:top-24"
          >
            <div className="card p-5 sm:p-6">
              <h2 className="text-lg font-bold text-[var(--color-text-primary)] mb-5">
                Generer lærermanual
              </h2>
              <BriefForm
                onBriefGenerated={handleBriefGenerated}
                onLoadingChange={handleLoadingChange}
              />
            </div>
          </motion.div>

          {/* Result column */}
          <div ref={resultRef} className="min-w-0">
            {isLoading && <LoadingSkeleton />}

            {currentBrief && !isLoading && (
              <BriefDisplay brief={currentBrief} />
            )}

            {!currentBrief && !isLoading && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
                className="card flex flex-col items-center justify-center py-16 sm:py-24 px-6 text-center"
              >
                <div className="flex h-16 w-16 items-center justify-center rounded-2xl bg-[var(--color-brand-50)] mb-4">
                  <BookOpenCheck
                    size={32}
                    className="text-[var(--color-brand-500)]"
                  />
                </div>
                <h3 className="text-base font-semibold text-[var(--color-text-primary)] mb-1.5">
                  Din lærermanual vises her
                </h3>
                <p className="text-sm text-[var(--color-text-muted)] max-w-xs">
                  Velg fag, trinn og tema til venstre for å generere en
                  strukturert undervisningsbrief.
                </p>
              </motion.div>
            )}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="mt-16 border-t border-[var(--color-border)] bg-[var(--color-surface)]">
        <div className="mx-auto max-w-6xl px-4 sm:px-6 py-8">
          <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-[var(--color-text-muted)]">
            <p>&copy; {new Date().getFullYear()} Prepp.ai. Alle rettigheter reservert.</p>
            <div className="flex gap-6">
              <a href="#" className="hover:text-[var(--color-text-secondary)] transition-colors">Personvern</a>
              <a href="#" className="hover:text-[var(--color-text-secondary)] transition-colors">Vilkår</a>
              <a href="#" className="hover:text-[var(--color-text-secondary)] transition-colors">Kontakt</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
}
