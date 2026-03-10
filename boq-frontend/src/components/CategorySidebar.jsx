import React from 'react';
import { motion } from 'framer-motion';
import { ListFilter } from 'lucide-react';

const CATEGORY_COLORS = {
    electrical: '#3B82F6',
    mechanical: '#F59E0B',
    piping: '#10B981',
    civil: '#8B5CF6',
    instrumentation: '#EC4899',
    structural: '#F97316',
    hvac: '#06B6D4',
    uncategorized: '#64748B',
};

function getCategoryColor(category) {
    const key = category.toLowerCase();
    for (const [cat, color] of Object.entries(CATEGORY_COLORS)) {
        if (key.includes(cat)) return color;
    }
    return CATEGORY_COLORS.uncategorized;
}

export default function CategorySidebar({ categories, activeCategory, onCategoryChange }) {
    const totalItems = Object.values(categories).reduce((sum, items) => sum + items.length, 0);

    return (
        <motion.div
            initial={{ opacity: 0, x: -16 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="card-industrial p-5"
        >
            <h3 className="text-xs font-mono font-medium text-text-muted uppercase tracking-widest mb-4 flex items-center gap-2">
                <ListFilter size={14} className="text-amber" />
                Categories
            </h3>

            <div className="space-y-1.5">
                {/* All categories */}
                <button
                    onClick={() => onCategoryChange(null)}
                    className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition-all text-sm ${activeCategory === null
                            ? 'bg-amber-subtle border border-amber/20 text-amber'
                            : 'hover:bg-surface-hover text-text-secondary hover:text-text-primary border border-transparent'
                        }`}
                >
                    <span className="font-medium">All items</span>
                    <span className="font-mono text-xs px-2 py-0.5 rounded-md bg-surface border border-border">
                        {totalItems}
                    </span>
                </button>

                {Object.entries(categories).map(([cat, items], idx) => {
                    const color = getCategoryColor(cat);
                    const isActive = activeCategory === cat;

                    return (
                        <motion.button
                            key={cat}
                            initial={{ opacity: 0, x: -8 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: 0.3 + idx * 0.05 }}
                            onClick={() => onCategoryChange(cat)}
                            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-left transition-all text-sm group ${isActive
                                    ? 'bg-surface-hover border border-border-light text-text-primary'
                                    : 'hover:bg-surface-hover text-text-secondary hover:text-text-primary border border-transparent'
                                }`}
                        >
                            <div className="flex items-center gap-2.5 min-w-0">
                                <div
                                    className="w-2 h-2 rounded-full shrink-0 transition-transform group-hover:scale-125"
                                    style={{ backgroundColor: color }}
                                />
                                <span className="capitalize truncate font-medium">{cat}</span>
                            </div>
                            <span
                                className="font-mono text-xs px-2 py-0.5 rounded-md shrink-0 transition-colors"
                                style={{
                                    backgroundColor: isActive ? `${color}20` : 'var(--color-surface)',
                                    border: `1px solid ${isActive ? `${color}40` : 'var(--color-border)'}`,
                                    color: isActive ? color : 'var(--color-text-muted)',
                                }}
                            >
                                {items.length}
                            </span>
                        </motion.button>
                    );
                })}
            </div>
        </motion.div>
    );
}

export { getCategoryColor };
