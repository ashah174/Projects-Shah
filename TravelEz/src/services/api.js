import axios from "axios";

const API = axios.create({
  baseURL: "http://localhost:5001/api",
});

export const getItineraries = () => API.get("/itineraries");
export const getPublicItineraries = () => API.get("/itineraries/public");
export const searchItineraries = (destination) =>
  API.get(`/itineraries/search?destination=${destination}`);
export const getItineraryById = (id) => API.get(`/itineraries/${id}`);
export const createItinerary = (data) => API.post("/itineraries", data);
export const updateItinerary = (id, data) => API.put(`/itineraries/${id}`, data);
export const deleteItinerary = (id) => API.delete(`/itineraries/${id}`);
export const addCommentToItinerary = (id, data) =>
  API.post(`/itineraries/${id}/comments`, data);
export const updateCommentOnItinerary = (id, commentId, data) =>
  API.put(`/itineraries/${id}/comments/${commentId}`, data);
export const deleteCommentFromItinerary = (id, commentId) =>
  API.delete(`/itineraries/${id}/comments/${commentId}`);
export const updateItineraryPrivacy = (id, isPublic) =>
  API.put(`/itineraries/${id}`, { isPublic });


export default API;