"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Menu,
  X,
  GraduationCap,
  Sparkles,
  LogIn,
} from "lucide-react";

const NAV_LINKS = [
  { label: "Om", href: "#om" },
  { label: "Priser", href: "#priser" },
  { label: "Kontakt", href: "#kontakt" },
];

export default function Header() {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <header className="sticky top-0 z-50 glass border-b border-[var(--color-border)]">
      <div className="mx-auto max-w-6xl px-4 sm:px-6">
        <div className="flex h-16 items-center justify-between">
          {/* Logo */}
          <a href="/" className="flex items-center gap-2 group">
            <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-[var(--color-brand-600)] text-white shadow-sm transition-transform group-hover:scale-105">
              <GraduationCap size={20} />
            </div>
            <span className="text-lg font-bold tracking-tight text-[var(--color-text-primary)]">
              Prepp<span className="text-[var(--color-brand-600)]">.ai</span>
            </span>
          </a>

          {/* Desktop nav */}
          <nav className="hidden md:flex items-center gap-1">
            {NAV_LINKS.map((link) => (
              <a
                key={link.label}
                href={link.href}
                className="px-3 py-2 rounded-lg text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-sunken)] transition-colors"
              >
                {link.label}
              </a>
            ))}
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center gap-2">
            <button className="px-4 py-2 rounded-lg text-sm font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-sunken)] transition-colors flex items-center gap-1.5">
              <LogIn size={16} />
              Logg inn
            </button>
            <button className="px-4 py-2.5 rounded-xl text-sm font-semibold text-white bg-[var(--color-brand-600)] hover:bg-[var(--color-brand-700)] shadow-sm hover:shadow-md transition-all flex items-center gap-1.5">
              <Sparkles size={16} />
              Kom i gang
            </button>
          </div>

          {/* Mobile menu button */}
          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="md:hidden flex h-10 w-10 items-center justify-center rounded-xl hover:bg-[var(--color-surface-sunken)] transition-colors"
            aria-label={mobileOpen ? "Lukk meny" : "Åpne meny"}
          >
            {mobileOpen ? <X size={22} /> : <Menu size={22} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      <AnimatePresence>
        {mobileOpen && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.2, ease: "easeInOut" }}
            className="md:hidden overflow-hidden border-t border-[var(--color-border)]"
          >
            <div className="px-4 py-4 space-y-1 bg-[var(--color-surface)]">
              {NAV_LINKS.map((link) => (
                <a
                  key={link.label}
                  href={link.href}
                  onClick={() => setMobileOpen(false)}
                  className="block px-4 py-3 rounded-xl text-base font-medium text-[var(--color-text-secondary)] hover:text-[var(--color-text-primary)] hover:bg-[var(--color-surface-sunken)] transition-colors"
                >
                  {link.label}
                </a>
              ))}
              <div className="pt-3 mt-2 border-t border-[var(--color-border)] space-y-2">
                <button className="w-full px-4 py-3 rounded-xl text-base font-medium text-[var(--color-text-secondary)] hover:bg-[var(--color-surface-sunken)] transition-colors flex items-center gap-2">
                  <LogIn size={18} />
                  Logg inn
                </button>
                <button className="w-full px-4 py-3 rounded-xl text-base font-semibold text-white bg-[var(--color-brand-600)] hover:bg-[var(--color-brand-700)] transition-colors flex items-center justify-center gap-2">
                  <Sparkles size={18} />
                  Kom i gang
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </header>
  );
}
