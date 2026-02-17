"use client";

import { motion } from "framer-motion";
import { Loader2 } from "lucide-react";

const SECTION_NAMES = [
  "Læreplankobling",
  "Faglig dybde",
  "Pedagogiske tips",
  "Elevspørsmål og feller",
  "Kilder",
];

export default function LoadingSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-3"
    >
      {/* Header skeleton */}
      <div className="rounded-2xl bg-gradient-to-br from-[var(--color-brand-600)] via-[var(--color-brand-700)] to-[var(--color-brand-800)] p-5 sm:p-6 shadow-lg">
        <div className="flex items-center justify-center gap-3 py-4">
          <Loader2 size={24} className="animate-spin text-white/80" />
          <div>
            <p className="text-base font-semibold text-white">Genererer lærermanual...</p>
            <p className="text-xs text-white/60 mt-0.5">
              AI analyserer læreplan og faginnhold
            </p>
          </div>
        </div>
      </div>

      {/* Section skeletons */}
      {SECTION_NAMES.map((name, idx) => (
        <motion.div
          key={name}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: idx * 0.1 }}
          className="card px-4 py-3.5 sm:px-5 sm:py-4"
        >
          <div className="flex items-center gap-3">
            <div className="h-9 w-9 rounded-xl skeleton" />
            <div className="flex-1 space-y-1.5">
              <div className="h-3.5 w-32 rounded skeleton" />
              <div className="h-2.5 w-48 rounded skeleton" />
            </div>
          </div>
        </motion.div>
      ))}
    </motion.div>
  );
}
