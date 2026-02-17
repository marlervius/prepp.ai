"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  BookOpen,
  Microscope,
  Lightbulb,
  HelpCircle,
  LinkIcon,
  ChevronDown,
  Clock,
  FileDown,
  Search,
  Bookmark,
  ExternalLink,
} from "lucide-react";
import type { Brief } from "@/types/brief";

interface BriefDisplayProps {
  brief: Brief;
}

const SECTION_CONFIG = [
  { id: "lk20_kobling", title: "Læreplankobling", icon: BookOpen, color: "text-blue-600", bg: "bg-blue-50" },
  { id: "faglig_dybde", title: "Faglig dybde", icon: Microscope, color: "text-purple-600", bg: "bg-purple-50" },
  { id: "pedagogiske_tips", title: "Pedagogiske tips", icon: Lightbulb, color: "text-amber-600", bg: "bg-amber-50" },
  { id: "elev_sporsmal_feller", title: "Elevspørsmål og feller", icon: HelpCircle, color: "text-rose-600", bg: "bg-rose-50" },
  { id: "kilder", title: "Kilder", icon: LinkIcon, color: "text-emerald-600", bg: "bg-emerald-50" },
] as const;

function SectionBlock({
  section,
  content,
  defaultOpen = false,
}: {
  section: (typeof SECTION_CONFIG)[number];
  content: string;
  defaultOpen?: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const Icon = section.icon;

  return (
    <div className="card overflow-hidden">
      <button
        onClick={() => setOpen(!open)}
        className="flex w-full items-center gap-3 px-4 py-3.5 sm:px-5 sm:py-4 text-left transition-colors hover:bg-[var(--color-surface-raised)]"
        aria-expanded={open}
      >
        <div className={`flex h-9 w-9 shrink-0 items-center justify-center rounded-xl ${section.bg}`}>
          <Icon size={18} className={section.color} />
        </div>
        <h3 className="flex-1 text-sm sm:text-base font-semibold text-[var(--color-text-primary)]">
          {section.title}
        </h3>
        <ChevronDown
          size={18}
          className={`shrink-0 text-[var(--color-text-muted)] transition-transform duration-200 ${
            open ? "rotate-180" : ""
          }`}
        />
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0 }}
            animate={{ height: "auto" }}
            exit={{ height: 0 }}
            transition={{ duration: 0.25, ease: [0.4, 0, 0.2, 1] }}
            className="overflow-hidden"
          >
            <div className="px-4 pb-4 sm:px-5 sm:pb-5 pt-0">
              <div className="border-t border-[var(--color-border-subtle)] pt-3.5">
                <div className="prose text-sm sm:text-[0.925rem] leading-relaxed">
                  {content.split("\n").map((paragraph, idx) =>
                    paragraph.trim() ? (
                      <p key={idx}>{paragraph}</p>
                    ) : null
                  )}
                </div>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default function BriefDisplay({ brief }: BriefDisplayProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, ease: "easeOut" }}
      className="space-y-3"
    >
      {/* Header card */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-[var(--color-brand-600)] via-[var(--color-brand-700)] to-[var(--color-brand-800)] p-5 sm:p-6 text-white shadow-lg">
        {/* Background pattern */}
        <div className="absolute inset-0 opacity-10">
          <div className="absolute -right-8 -top-8 h-40 w-40 rounded-full bg-white/20" />
          <div className="absolute -left-4 -bottom-4 h-24 w-24 rounded-full bg-white/10" />
        </div>

        <div className="relative">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
            <div>
              <div className="inline-flex items-center gap-1.5 rounded-full bg-white/15 px-3 py-1 text-xs font-medium backdrop-blur-sm mb-2">
                <BookOpen size={12} />
                Lærermanual
              </div>
              <h2 className="text-xl sm:text-2xl font-bold">
                {brief.subject}
              </h2>
              <p className="mt-1 text-sm text-white/80">
                Trinn {brief.grade} &middot; {brief.topic}
              </p>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-white/70 sm:text-right">
              <Clock size={14} />
              {Math.round(brief.processing_time_ms / 1000)}s
            </div>
          </div>
        </div>
      </div>

      {/* Sections */}
      {SECTION_CONFIG.map((section, idx) => (
        <SectionBlock
          key={section.id}
          section={section}
          content={brief.content[section.id]}
          defaultOpen={idx === 0}
        />
      ))}

      {/* Sources */}
      {brief.sources && brief.sources.length > 0 && (
        <div className="card p-4 sm:p-5">
          <h4 className="text-xs font-semibold uppercase tracking-wider text-[var(--color-text-muted)] mb-3">
            Primærkilder ({brief.sources.length})
          </h4>
          <div className="space-y-2">
            {brief.sources.map((source, idx) => (
              <a
                key={idx}
                href={source.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm transition-colors hover:bg-[var(--color-surface-sunken)] group"
              >
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-[var(--color-surface-sunken)] text-[var(--color-text-muted)] group-hover:bg-[var(--color-brand-50)] group-hover:text-[var(--color-brand-600)] transition-colors">
                  <ExternalLink size={14} />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-[var(--color-text-primary)] truncate">
                    {source.title || source.url}
                  </p>
                  <p className="text-xs text-[var(--color-text-muted)]">
                    {source.source.toUpperCase()}
                  </p>
                </div>
              </a>
            ))}
          </div>
        </div>
      )}

      {/* Action bar */}
      <div className="card p-3 sm:p-4">
        <div className="flex flex-col sm:flex-row gap-2">
          <button className="flex-1 flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2.5 text-sm font-medium text-[var(--color-text-secondary)] shadow-[var(--shadow-xs)] transition-all hover:bg-[var(--color-surface-raised)] hover:shadow-sm active:scale-[0.98]">
            <FileDown size={16} />
            Eksporter PDF
          </button>
          <button className="flex-1 flex items-center justify-center gap-2 rounded-xl border border-[var(--color-border)] bg-[var(--color-surface)] px-4 py-2.5 text-sm font-medium text-[var(--color-text-secondary)] shadow-[var(--shadow-xs)] transition-all hover:bg-[var(--color-surface-raised)] hover:shadow-sm active:scale-[0.98]">
            <Search size={16} />
            Grav dypere
          </button>
          <button className="flex-1 flex items-center justify-center gap-2 rounded-xl border border-[var(--color-brand-200)] bg-[var(--color-brand-50)] px-4 py-2.5 text-sm font-medium text-[var(--color-brand-700)] shadow-[var(--shadow-xs)] transition-all hover:bg-[var(--color-brand-100)] hover:shadow-sm active:scale-[0.98]">
            <Bookmark size={16} />
            Lagre
          </button>
        </div>
      </div>
    </motion.div>
  );
}
