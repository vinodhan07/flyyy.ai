import React from 'react';
import { motion } from 'framer-motion';
import { getCategoryColor } from './CategorySidebar';

export default function DataTable({ items, activeCategory }) {
    const filtered = activeCategory
        ? items.filter(item => item.category === activeCategory)
        : items;

    return (
        <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.25 }}
            className="card-industrial overflow-hidden"
        >
            <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="frosted-header sticky top-0 z-10">
                            <th className="w-8 px-2 py-4 border-b border-border" />
                            <th className="px-5 py-4 text-[10px] font-mono font-medium text-text-muted uppercase tracking-widest border-b border-border">
                                Description
                            </th>
                            <th className="px-5 py-4 text-[10px] font-mono font-medium text-text-muted uppercase tracking-widest border-b border-border">
                                Brand
                            </th>
                            <th className="px-5 py-4 text-[10px] font-mono font-medium text-text-muted uppercase tracking-widest border-b border-border text-right">
                                Qty
                            </th>
                            <th className="px-5 py-4 text-[10px] font-mono font-medium text-text-muted uppercase tracking-widest border-b border-border">
                                Unit
                            </th>
                            <th className="px-5 py-4 text-[10px] font-mono font-medium text-text-muted uppercase tracking-widest border-b border-border">
                                Category
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {filtered.map((item, idx) => {
                            const catColor = getCategoryColor(item.category || 'uncategorized');
                            return (
                                <motion.tr
                                    key={idx}
                                    initial={{ opacity: 0, x: -8 }}
                                    animate={{ opacity: 1, x: 0 }}
                                    transition={{
                                        delay: Math.min(idx * 0.025, 1.2),
                                        duration: 0.35,
                                        ease: [0.22, 1, 0.36, 1],
                                    }}
                                    className="group transition-colors hover:bg-surface-hover/50 relative"
                                >
                                    {/* Color indicator */}
                                    <td className="relative px-2 py-3.5">
                                        <div
                                            className="row-indicator"
                                            style={{ backgroundColor: catColor }}
                                        />
                                    </td>

                                    {/* Description */}
                                    <td className="px-5 py-3.5 text-sm text-text-primary">
                                        <div className="max-w-md leading-relaxed">{item.description}</div>
                                    </td>

                                    {/* Brand */}
                                    <td className="px-5 py-3.5 text-sm text-text-muted italic font-light">
                                        {item.brand || 'Generic'}
                                    </td>

                                    {/* Quantity */}
                                    <td className="px-5 py-3.5 text-right">
                                        <span className="font-mono text-sm font-medium text-amber">
                                            {item.quantity}
                                        </span>
                                    </td>

                                    {/* Unit */}
                                    <td className="px-5 py-3.5 text-sm text-text-muted font-mono">
                                        {item.unit || '—'}
                                    </td>

                                    {/* Category Pill */}
                                    <td className="px-5 py-3.5">
                                        <span
                                            className="category-pill"
                                            style={{
                                                backgroundColor: `${catColor}15`,
                                                borderColor: `${catColor}30`,
                                                color: catColor,
                                            }}
                                        >
                                            {item.category || 'uncategorized'}
                                        </span>
                                    </td>
                                </motion.tr>
                            );
                        })}
                    </tbody>
                </table>

                {filtered.length === 0 && (
                    <div className="py-16 text-center text-text-muted text-sm font-mono">
                        No items in this category
                    </div>
                )}
            </div>

            {/* Footer */}
            <div className="px-5 py-3 border-t border-border flex items-center justify-between">
                <span className="text-xs text-text-muted font-mono">
                    {filtered.length} item{filtered.length !== 1 ? 's' : ''}
                    {activeCategory ? ` in ${activeCategory}` : ' total'}
                </span>
                <span className="text-xs text-text-muted font-mono">
                    BOQ.AI
                </span>
            </div>
        </motion.div>
    );
}
