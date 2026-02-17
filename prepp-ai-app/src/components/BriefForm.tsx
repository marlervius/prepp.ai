"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen,
  GraduationCap,
  MessageSquareText,
  Sparkles,
  AlertCircle,
  CheckCircle2,
  Loader2,
} from "lucide-react";
import type { Brief } from "@/types/brief";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface BriefFormProps {
  onBriefGenerated: (brief: Brief) => void;
  onLoadingChange: (loading: boolean) => void;
}

const SUBJECTS = [
  "Norsk", "Matematikk", "Engelsk", "Naturfag", "Samfunnsfag",
  "Historie", "Geografi", "Religion og etikk", "Kunst og håndverk",
  "Musikk", "Kroppsøving", "Fysikk", "Kjemi", "Biologi",
];

const GRADES = [
  "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
  "VG1", "VG2", "VG3",
];

const FEATURES = [
  "Læreplankobling til LK20",
  "Faglig dybde og kontekst",
  "Pedagogiske tips",
  "Forventede elevspørsmål",
  "Kildehenvisninger",
];

export default function BriefForm({ onBriefGenerated, onLoadingChange }: BriefFormProps) {
  const [formData, setFormData] = useState({ subject: "", grade: "", topic: "" });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");

  const filledCount = [formData.subject, formData.grade, formData.topic].filter(Boolean).length;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.subject || !formData.grade || !formData.topic) {
      setError("Vennligst fyll inn alle feltene");
      return;
    }

    setIsSubmitting(true);
    setError("");
    onLoadingChange(true);

    try {
      const response = await fetch(`${API_URL}/api/v1/briefs`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) throw new Error(`API error: ${response.status}`);

      const brief = await response.json();
      onBriefGenerated(brief);
    } catch {
      setError("Kunne ikke generere brief. Prøv igjen senere.");
      onLoadingChange(false);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleChange = (field: string, value: string) => {
    setFormData((prev) => ({ ...prev, [field]: value }));
    if (error) setError("");
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-5">
      {/* Progress indicator */}
      <div className="flex items-center gap-2">
        {[1, 2, 3].map((step) => (
          <div key={step} className="flex items-center gap-2 flex-1">
            <div
              className={`h-1.5 flex-1 rounded-full transition-colors duration-300 ${
                filledCount >= step
                  ? "bg-[var(--color-brand-500)]"
                  : "bg-[var(--color-border)]"
              }`}
            />
          </div>
        ))}
        <span className="text-xs font-medium text-[var(--color-text-muted)] ml-1 tabular-nums">
          {filledCount}/3
        </span>
      </div>

      {/* Subject */}
      <div className="space-y-1.5">
        <label htmlFor="subject" className="flex items-center gap-1.5 text-sm font-medium text-[var(--color-text-primary)]">
          <BookOpen size={15} className="text-[var(--color-brand-500)]" />
          Fag
        </label>
        <select
          id="subject"
          value={formData.subject}
          onChange={(e) => handleChange("subject", e.target.value)}
          disabled={isSubmitting}
          className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 text-sm text-[var(--color-text-primary)] shadow-[var(--shadow-xs)] transition-all hover:border-[var(--color-brand-300)] focus:border-[var(--color-brand-500)] focus:ring-2 focus:ring-[var(--color-brand-100)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E")`,
            backgroundRepeat: "no-repeat",
            backgroundPosition: "right 12px center",
          }}
        >
          <option value="">Velg fag...</option>
          {SUBJECTS.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Grade */}
      <div className="space-y-1.5">
        <label htmlFor="grade" className="flex items-center gap-1.5 text-sm font-medium text-[var(--color-text-primary)]">
          <GraduationCap size={15} className="text-[var(--color-brand-500)]" />
          Trinn
        </label>
        <select
          id="grade"
          value={formData.grade}
          onChange={(e) => handleChange("grade", e.target.value)}
          disabled={isSubmitting}
          className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 text-sm text-[var(--color-text-primary)] shadow-[var(--shadow-xs)] transition-all hover:border-[var(--color-brand-300)] focus:border-[var(--color-brand-500)] focus:ring-2 focus:ring-[var(--color-brand-100)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed appearance-none"
          style={{
            backgroundImage: `url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='%2394a3b8' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='m6 9 6 6 6-6'/%3E%3C/svg%3E")`,
            backgroundRepeat: "no-repeat",
            backgroundPosition: "right 12px center",
          }}
        >
          <option value="">Velg trinn...</option>
          {GRADES.map((g) => (
            <option key={g} value={g}>
              {g.startsWith("VG") ? g : `${g}. trinn`}
            </option>
          ))}
        </select>
      </div>

      {/* Topic */}
      <div className="space-y-1.5">
        <label htmlFor="topic" className="flex items-center gap-1.5 text-sm font-medium text-[var(--color-text-primary)]">
          <MessageSquareText size={15} className="text-[var(--color-brand-500)]" />
          Tema
        </label>
        <input
          type="text"
          id="topic"
          value={formData.topic}
          onChange={(e) => handleChange("topic", e.target.value)}
          placeholder="f.eks. fotosyntese, andre verdenskrig, brøker..."
          disabled={isSubmitting}
          maxLength={200}
          className="w-full rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-3 text-sm text-[var(--color-text-primary)] shadow-[var(--shadow-xs)] placeholder:text-[var(--color-text-muted)] transition-all hover:border-[var(--color-brand-300)] focus:border-[var(--color-brand-500)] focus:ring-2 focus:ring-[var(--color-brand-100)] focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed"
        />
        <p className="text-xs text-[var(--color-text-muted)]">Beskriv temaet du skal undervise i</p>
      </div>

      {/* Error */}
      <AnimatePresence>
        {error && (
          <motion.div
            initial={{ opacity: 0, y: -8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            className="flex items-start gap-2.5 rounded-xl border border-red-200 bg-red-50 px-4 py-3"
          >
            <AlertCircle size={16} className="mt-0.5 shrink-0 text-red-500" />
            <p className="text-sm text-red-700">{error}</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Submit */}
      <button
        type="submit"
        disabled={isSubmitting || filledCount < 3}
        className="group relative w-full rounded-xl bg-[var(--color-brand-600)] px-6 py-3.5 text-sm font-semibold text-white shadow-md transition-all hover:bg-[var(--color-brand-700)] hover:shadow-lg active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:shadow-md"
      >
        <span className="flex items-center justify-center gap-2">
          {isSubmitting ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Genererer...
            </>
          ) : (
            <>
              <Sparkles size={18} className="transition-transform group-hover:rotate-12" />
              Generer lærermanual
            </>
          )}
        </span>
      </button>

      {/* Features list */}
      <div className="rounded-xl border border-[var(--color-brand-100)] bg-[var(--color-brand-50)] p-4">
        <p className="text-xs font-semibold text-[var(--color-brand-700)] mb-2.5">
          Du får en komplett lærermanual med:
        </p>
        <ul className="space-y-1.5">
          {FEATURES.map((f) => (
            <li key={f} className="flex items-center gap-2 text-xs text-[var(--color-brand-800)]">
              <CheckCircle2 size={14} className="shrink-0 text-[var(--color-brand-500)]" />
              {f}
            </li>
          ))}
        </ul>
      </div>
    </form>
  );
}
