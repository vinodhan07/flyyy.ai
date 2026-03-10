import React from 'react';
import { motion } from 'framer-motion';
import { FileSpreadsheet, BarChart3, CheckCircle2, ChevronLeft } from 'lucide-react';
import CategorySidebar from './CategorySidebar';
import DataTable from './DataTable';

export default function ResultsDashboard({ data, activeCategory, onCategoryChange, onReset }) {
    const stats = [
        {
            label: 'Total Sheets',
            value: data.total_sheets,
            icon: FileSpreadsheet,
            glowClass: 'stat-glow-slate',
            accentColor: 'text-slate-400',
            bgColor: 'bg-slate-400/5',
        },
        {
            label: 'Analyzed',
            value: Array.isArray(data.sheets_with_data) ? data.sheets_with_data.length : data.sheets_with_data,
            icon: BarChart3,
            glowClass: 'stat-glow-amber',
            accentColor: 'text-amber',
            bgColor: 'bg-amber-subtle',
        },
        {
            label: 'Materials',
            value: data.extracted_items,
            icon: CheckCircle2,
            glowClass: 'stat-glow-emerald',
            accentColor: 'text-emerald',
            bgColor: 'bg-emerald-glow',
        },
    ];

    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
            className="space-y-8"
        >
            {/* Top Bar: Back + Stats */}
            <div className="flex flex-col lg:flex-row lg:items-start justify-between gap-6">
                {/* Back button + Title */}
                <motion.div
                    initial={{ opacity: 0, x: -12 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: 0.1 }}
                    className="flex items-center gap-4"
                >
                    <button
                        onClick={onReset}
                        className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-text-muted hover:text-amber hover:bg-amber-subtle border border-transparent hover:border-amber/20 transition-all text-sm font-mono"
                    >
                        <ChevronLeft size={16} />
                        <span>Back</span>
                    </button>
                    <div className="h-5 w-px bg-border" />
                    <h2 className="text-xl font-display font-semibold text-text-primary tracking-tight">
                        Extraction Results
                    </h2>
                </motion.div>

                {/* Stats */}
                <div className="grid grid-cols-3 gap-3">
                    {stats.map((stat, idx) => (
                        <motion.div
                            key={stat.label}
                            initial={{ opacity: 0, y: 8 }}
                            animate={{ opacity: 1, y: 0 }}
                            transition={{ delay: 0.15 + idx * 0.08 }}
                            className={`card-industrial ${stat.glowClass} px-4 py-3 flex flex-col gap-1`}
                        >
                            <span className="text-[9px] font-mono uppercase tracking-widest text-text-muted font-medium">
                                {stat.label}
                            </span>
                            <div className="flex items-center gap-2">
                                <stat.icon size={15} className={stat.accentColor} strokeWidth={1.8} />
                                <span className={`font-mono text-xl font-medium ${stat.accentColor}`}>
                                    {stat.value}
                                </span>
                            </div>
                        </motion.div>
                    ))}
                </div>
            </div>

            {/* Main Content: Sidebar + Table */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
                {/* Sidebar */}
                <div className="lg:col-span-1">
                    <CategorySidebar
                        categories={data.categories || {}}
                        activeCategory={activeCategory}
                        onCategoryChange={onCategoryChange}
                    />
                </div>

                {/* Table */}
                <div className="lg:col-span-4">
                    <DataTable
                        items={data.items || []}
                        activeCategory={activeCategory}
                    />
                </div>
            </div>
        </motion.div>
    );
}
