import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Upload, FileSpreadsheet, CheckCircle2, AlertCircle, Loader2, ChevronRight, BarChart3, ListFilter } from 'lucide-react';
import { boqService } from './services/BoqService';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && (selectedFile.name.endsWith('.xlsx') || selectedFile.name.endsWith('.xls'))) {
      setFile(selectedFile);
      setError(null);
    } else {
      setError('Please select a valid Excel file (.xlsx or .xls)');
      setFile(null);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);
    setUploadProgress(10);

    try {
      const data = await boqService.extract(file);
      setUploadProgress(100);
      setResults(data);
    } catch (err) {
      console.error(err);
      const detail = err?.response?.data?.detail || err?.message || 'Unknown error';
      setError(`Extraction failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-8 text-text-primary">
      <header className="max-w-6xl mx-auto mb-12 flex items-center justify-between">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <div className="p-3 rounded-2xl bg-primary/10 border border-primary/20 glow-primary">
            <FileSpreadsheet className="text-primary w-8 h-8" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight">BOQ.AI</h1>
            <p className="text-text-secondary text-sm">Intelligent Bill of Quantities Extraction</p>
          </div>
        </motion.div>
      </header>

      <main className="max-w-6xl mx-auto space-y-8">
        {!results ? (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass-card rounded-3xl p-12 text-center max-w-2xl mx-auto"
          >
            <div className="mb-8 p-6 rounded-full bg-white/5 inline-block border border-white/10">
              <Upload className="w-12 h-12 text-primary mx-auto" />
            </div>
            <h2 className="text-2xl font-semibold mb-3">Upload your BOQ</h2>
            <p className="text-text-secondary mb-8">Drop your Excel file here or click to browse</p>

            <div className="relative group cursor-pointer mb-6">
              <input
                type="file"
                accept=".xlsx, .xls"
                onChange={handleFileChange}
                className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
              />
              <div className={`p-8 rounded-2xl border-2 border-dashed transition-all ${file ? 'border-primary bg-primary/5' : 'border-white/10 group-hover:border-primary/50 bg-white/5'}`}>
                {file ? (
                  <div className="flex items-center justify-center gap-3">
                    <CheckCircle2 className="text-primary" />
                    <span className="font-medium">{file.name}</span>
                  </div>
                ) : (
                  <span className="text-text-muted">Select an Excel file (.xlsx, .xls)</span>
                )}
              </div>
            </div>

            {error && (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex items-center gap-2 text-red-400 justify-center mb-6"
              >
                <AlertCircle size={18} />
                <span className="text-sm">{error}</span>
              </motion.div>
            )}

            <button
              onClick={handleUpload}
              disabled={!file || loading}
              className={`w-full py-4 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 ${!file || loading
                ? 'bg-white/5 text-text-muted cursor-not-allowed'
                : 'bg-primary hover:bg-primary/90 text-white glow-primary shadow-lg shadow-primary/25'
                }`}
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin" />
                  <span>Processing...</span>
                </>
              ) : (
                <>
                  <span>Extract Data</span>
                  <ChevronRight size={20} />
                </>
              )}
            </button>
          </motion.div>
        ) : (
          <ResultsDisplay data={results} onReset={() => setResults(null)} />
        )}
      </main>
    </div>
  );
}

function ResultsDisplay({ data, onReset }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="space-y-6"
    >
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-10 gap-6">
        <div className="flex items-center gap-4">
          <button
            onClick={onReset}
            className="text-text-secondary hover:text-text-primary transition-colors flex items-center gap-2 text-sm font-medium"
          >
            <ChevronRight className="rotate-180" size={16} />
            Back to Upload
          </button>
          <div className="h-4 w-px bg-white/10"></div>
          <h2 className="text-2xl font-bold">Extraction Results</h2>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="px-4 py-3 rounded-2xl bg-white/5 border border-white/10 flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-text-muted font-bold mb-1">Total Sheets</span>
            <div className="flex items-center gap-2">
              <FileSpreadsheet size={16} className="text-primary" />
              <span className="text-lg font-bold">{data.total_sheets}</span>
            </div>
          </div>
          <div className="px-4 py-3 rounded-2xl bg-primary/10 border border-primary/20 flex flex-col glow-primary">
            <span className="text-[10px] uppercase tracking-wider text-primary font-bold mb-1">Analyzed Sheets</span>
            <div className="flex items-center gap-2">
              <BarChart3 size={16} className="text-primary" />
              <span className="text-lg font-bold text-primary">{data.sheets_with_data}</span>
            </div>
          </div>
          <div className="px-4 py-3 rounded-2xl bg-green-500/10 border border-green-500/20 flex flex-col">
            <span className="text-[10px] uppercase tracking-wider text-green-400 font-bold mb-1">Total Materials</span>
            <div className="flex items-center gap-2">
              <CheckCircle2 size={16} className="text-green-400" />
              <span className="text-lg font-bold text-green-400">{data.extracted_items}</span>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1 space-y-6">
          <div className="glass-card rounded-2xl p-6">
            <h3 className="text-sm font-semibold text-text-secondary uppercase tracking-wider mb-4 flex items-center gap-2">
              <ListFilter size={16} />
              Categories
            </h3>
            <div className="space-y-2">
              {Object.entries(data.categories || {}).map(([cat, items]) => (
                <div key={cat} className="flex items-center justify-between p-3 rounded-xl bg-white/5 border border-transparent hover:border-white/10 transition-all cursor-pointer group">
                  <span className="text-sm font-medium capitalize group-hover:text-primary transition-colors">{cat}</span>
                  <span className="px-2 py-0.5 rounded-full bg-white/10 text-xs font-mono">{items.length}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div className="glass-card rounded-2xl overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-white/5">
                    <th className="px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider border-b border-white/10 w-1/3">Description</th>
                    <th className="px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider border-b border-white/10">Brand</th>
                    <th className="px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider border-b border-white/10 text-right">Quantity</th>
                    <th className="px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider border-b border-white/10">Unit</th>
                    <th className="px-6 py-4 text-xs font-semibold text-text-secondary uppercase tracking-wider border-b border-white/10">Category</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-white/10">
                  {data.items.map((item, idx) => (
                    <motion.tr
                      key={idx}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: Math.min(idx * 0.03, 1.5) }}
                      className="hover:bg-white/[0.02] transition-colors group"
                    >
                      <td className="px-6 py-4 text-sm font-medium">
                        <div className="max-w-md break-words">{item.description}</div>
                      </td>
                      <td className="px-6 py-4 text-sm text-text-secondary italic">{item.brand || 'Generic'}</td>
                      <td className="px-6 py-4 text-sm font-mono text-primary text-right">{item.quantity}</td>
                      <td className="px-6 py-4 text-sm text-text-secondary">{item.unit || '-'}</td>
                      <td className="px-6 py-4 text-sm">
                        <span className="px-2 py-1 rounded-md bg-white/5 border border-white/10 text-xs capitalize text-text-secondary group-hover:text-text-primary group-hover:border-primary/30 transition-all">
                          {item.category || 'uncategorized'}
                        </span>
                      </td>
                    </motion.tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}

export default App;
