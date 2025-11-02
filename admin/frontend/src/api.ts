import axios from 'axios';
import type { Rabbi, RabbiCreate, RabbiUpdate, Series, SeriesCreate, SeriesUpdate } from './types';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Rabbi API
export const rabbisApi = {
  getAll: () => api.get<Rabbi[]>('/rabbis/'),
  getById: (id: number) => api.get<Rabbi>(`/rabbis/${id}`),
  create: (data: RabbiCreate) => api.post<Rabbi>('/rabbis/', data),
  update: (id: number, data: RabbiUpdate) => api.put<Rabbi>(`/rabbis/${id}`, data),
  delete: (id: number) => api.delete(`/rabbis/${id}`),
};

// Series API
export const seriesApi = {
  getAll: () => api.get<Series[]>('/series/'),
  getByRabbi: (rabbiId: number) => api.get<Series[]>(`/series/by-rabbi/${rabbiId}`),
  getById: (id: number) => api.get<Series>(`/series/${id}`),
  create: (data: SeriesCreate) => api.post<Series>('/series/', data),
  update: (id: number, data: SeriesUpdate) => api.put<Series>(`/series/${id}`, data),
  delete: (id: number) => api.delete(`/series/${id}`),
};
