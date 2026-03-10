import React, { useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
    Upload,
    CheckCircle2,
    AlertCircle,
    Loader2,
    ChevronRight,
    FileSpreadsheet,
    FileText,
    File,
} from 'lucide-react';

const FILE_TYPES = [
    { ext: '.xlsx', icon: FileSpreadsheet, label: 'Excel' },
    { ext: '.xls', icon: FileSpreadsheet, label: 'Excel' },
    { ext: '.csv', icon: FileText, label: 'CSV' },
    { ext: '.pdf', icon: File, label: 'PDF' },
    { ext: '.docx', icon: FileText, label: 'Word' },
];

export default function UploadZone({ file, onFileChange, onUpload, loading, error }) {
    const inputRef = useRef(null);
    const [isDragging, setIsDragging] = useState(false);

    const ALLOWED_TYPES = ['.xlsx', '.xls', '.csv', '.pdf', '.docx'];

    const handleDragOver = (e) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile && ALLOWED_TYPES.some(ext => droppedFile.name.toLowerCase().endsWith(ext))) {
            onFileChange(droppedFile);
        }
    };

    const handleInputChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile && ALLOWED_TYPES.some(ext => selectedFile.name.toLowerCase().endsWith(ext))) {
            onFileChange(selectedFile);
        }
    };

    const getFileIcon = () => {
        if (!file) return null;
        const match = FILE_TYPES.find(ft => file.name.toLowerCase().endsWith(ft.ext));
        return match ? match.icon : File;
    };

    const FileIcon = getFileIcon();

    return (
        <motion.div
            initial={{ opacity: 0, y: 24 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.15, ease: [0.22, 1, 0.36, 1] }}
            className="card-industrial max-w-2xl mx-auto p-10"
        >
            {/* Title */}
            <div className="text-center mb-8">
                <h2 className="font-display text-2xl font-semibold text-text-primary mb-2">
                    Upload your document
                </h2>
                <p className="text-text-muted text-sm">
                    Drop a BOQ file and we'll extract every material, quantity and category
                </p>
            </div>

            {/* Drop zone */}
            <div
                onClick={() => inputRef.current?.click()}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`upload-zone cursor-pointer p-10 text-center ${file ? 'has-file' : ''} ${isDragging ? 'border-amber bg-amber-subtle' : ''}`}
            >
                <input
                    ref={inputRef}
                    type="file"
                    accept=".xlsx,.xls,.csv,.pdf,.docx"
                    onChange={handleInputChange}
                    className="hidden"
                />

                <AnimatePresence mode="wait">
                    {file ? (
                        <motion.div
                            key="file-selected"
                            initial={{ opacity: 0, scale: 0.95 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0, scale: 0.95 }}
                            className="flex flex-col items-center gap-3"
                        >
                            <div className="p-3 rounded-xl bg-amber/10 border border-amber/20">
                                {FileIcon && <FileIcon className="w-8 h-8 text-amber" strokeWidth={1.5} />}
                            </div>
                            <div>
                                <p className="font-mono text-sm text-amber font-medium">{file.name}</p>
                                <p className="text-text-muted text-xs mt-1">
                                    {(file.size / 1024).toFixed(1)} KB — Ready to extract
                                </p>
                            </div>
                            <div className="flex items-center gap-1.5 text-emerald text-xs font-mono mt-1">
                                <CheckCircle2 size={14} />
                                <span>File accepted</span>
                            </div>
                        </motion.div>
                    ) : (
                        <motion.div
                            key="no-file"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            exit={{ opacity: 0 }}
                            className="flex flex-col items-center gap-4"
                        >
                            <div className="p-4 rounded-2xl bg-surface border border-border">
                                <Upload className="w-8 h-8 text-text-muted" strokeWidth={1.5} />
                            </div>
                            <div>
                                <p className="text-text-secondary text-sm font-medium">
                                    {isDragging ? 'Drop your file here' : 'Click to browse or drag & drop'}
                                </p>
                                <p className="text-text-muted text-xs mt-1 font-mono">
                                    .xlsx · .xls · .csv · .pdf · .docx
                                </p>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </div>

            {/* Error */}
            <AnimatePresence>
                {error && (
                    <motion.div
                        initial={{ opacity: 0, height: 0 }}
                        animate={{ opacity: 1, height: 'auto' }}
                        exit={{ opacity: 0, height: 0 }}
                        className="warning-stripe px-4 py-3 mt-4 flex items-center gap-2"
                    >
                        <AlertCircle size={16} className="text-danger shrink-0" />
                        <span className="text-sm text-danger/90">{error}</span>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Upload Button */}
            <motion.button
                whileHover={file && !loading ? { scale: 1.01 } : {}}
                whileTap={file && !loading ? { scale: 0.99 } : {}}
                onClick={onUpload}
                disabled={!file || loading}
                className="btn-primary w-full py-4 mt-6 flex items-center justify-center gap-2.5 text-base"
            >
                {loading ? (
                    <>
                        <Loader2 className="animate-spin" size={20} />
                        <span className="font-mono text-sm">Processing extraction…</span>
                    </>
                ) : (
                    <>
                        <span>Extract Materials</span>
                        <ChevronRight size={18} />
                    </>
                )}
            </motion.button>
        </motion.div>
    );
}
