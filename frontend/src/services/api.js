import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8531/',
})

export default api;