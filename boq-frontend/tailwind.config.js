/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                base: {
                    DEFAULT: "#0C0E12",
                    light: "#12151B",
                },
                surface: {
                    DEFAULT: "#1A1D25",
                    hover: "#22252F",
                },
                border: {
                    DEFAULT: "#2A2E38",
                    light: "#363A46",
                },
                amber: {
                    DEFAULT: "#F59E0B",
                    dim: "#D97706",
                    glow: "rgba(245, 158, 11, 0.15)",
                    subtle: "rgba(245, 158, 11, 0.08)",
                },
                emerald: {
                    DEFAULT: "#10B981",
                    dim: "#059669",
                    glow: "rgba(16, 185, 129, 0.15)",
                },
                slate: {
                    400: "#94A3B8",
                    500: "#64748B",
                    600: "#475569",
                },
                danger: {
                    DEFAULT: "#EF4444",
                    glow: "rgba(239, 68, 68, 0.15)",
                },
                text: {
                    primary: "#F1F5F9",
                    secondary: "#94A3B8",
                    muted: "#64748B",
                },
            },
            fontFamily: {
                sans: ['Outfit', 'system-ui', '-apple-system', 'sans-serif'],
                mono: ['DM Mono', 'Fira Code', 'monospace'],
                display: ['Outfit', 'system-ui', 'sans-serif'],
            },
            backgroundImage: {
                'grid-dots': 'radial-gradient(circle at 1px 1px, rgba(245, 158, 11, 0.04) 1px, transparent 0)',
            },
            backgroundSize: {
                'grid-dots': '24px 24px',
            },
            boxShadow: {
                'amber-glow': '0 0 24px rgba(245, 158, 11, 0.12)',
                'emerald-glow': '0 0 24px rgba(16, 185, 129, 0.12)',
            },
            animation: {
                'scan': 'scanLine 3s ease-in-out infinite',
            },
        },
    },
    plugins: [],
}
