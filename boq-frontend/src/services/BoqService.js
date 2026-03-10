import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Adjust if backend runs on a different port

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 300000, // 5 minute timeout — AI extraction takes time for large files
});

export const boqService = {
    // AI-powered extraction: reads all sheets, chunks text, sends to Gemini
    extract: async (file, industry = 'construction') => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post(`/upload-excel?industry=${industry}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },

    // Heuristic extraction (faster but may miss items)
    extractHeuristic: async (file, industry = 'construction') => {
        const formData = new FormData();
        formData.append('file', file);

        const response = await api.post(`/extract?industry=${industry}`, formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return response.data;
    },
};
