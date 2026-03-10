import React from 'react';
import { motion } from 'framer-motion';
import { HardHat } from 'lucide-react';

export default function Header() {
    return (
        <header className="max-w-7xl mx-auto mb-10 px-6">
            <motion.div
                initial={{ opacity: 0, y: -12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
                className="flex items-center justify-between"
            >
                <div className="flex items-center gap-4">
                    <div className="relative p-3 rounded-xl bg-amber-subtle border border-amber/20">
                        <HardHat className="w-7 h-7 text-amber" strokeWidth={1.8} />
                        <div className="absolute -top-px -right-px w-2 h-2 rounded-full bg-amber animate-pulse" />
                    </div>
                    <div>
                        <h1 className="font-mono text-2xl font-medium tracking-wider text-text-primary">
                            BOQ<span className="text-amber">.AI</span>
                        </h1>
                        <p className="text-text-muted text-xs tracking-widest uppercase font-mono">
                            Intelligent Extraction Engine
                        </p>
                    </div>
                </div>

                <div className="hidden sm:flex items-center gap-3">
                    <span className="file-type-badge">.xlsx</span>
                    <span className="file-type-badge">.csv</span>
                    <span className="file-type-badge">.pdf</span>
                    <span className="file-type-badge">.docx</span>
                </div>
            </motion.div>

            {/* Measurement line */}
            <motion.div
                initial={{ scaleX: 0 }}
                animate={{ scaleX: 1 }}
                transition={{ duration: 0.8, delay: 0.3, ease: [0.22, 1, 0.36, 1] }}
                className="measurement-line mt-6"
            />
        </header>
    );
}
