import React, { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import Header from './components/Header';
import UploadZone from './components/UploadZone';
import ResultsDashboard from './components/ResultsDashboard';
import { boqService } from './services/BoqService';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [activeCategory, setActiveCategory] = useState(null);

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setError(null);
  };

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);

    try {
      const data = await boqService.extract(file);
      setResults(data);
    } catch (err) {
      console.error(err);
      const detail = err?.response?.data?.detail || err?.message || 'Unknown error';
      setError(`Extraction failed: ${detail}`);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setResults(null);
    setFile(null);
    setError(null);
    setActiveCategory(null);
  };

  return (
    <div className="min-h-screen py-8 px-4">
      <Header />

      <main className="max-w-7xl mx-auto px-2">
        <AnimatePresence mode="wait">
          {!results ? (
            <UploadZone
              key="upload"
              file={file}
              onFileChange={handleFileChange}
              onUpload={handleUpload}
              loading={loading}
              error={error}
            />
          ) : (
            <ResultsDashboard
              key="results"
              data={results}
              activeCategory={activeCategory}
              onCategoryChange={setActiveCategory}
              onReset={handleReset}
            />
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
