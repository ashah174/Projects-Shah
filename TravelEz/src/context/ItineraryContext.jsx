import { createContext, useContext, useState, useEffect } from "react";
import { getItineraries, updateItineraryPrivacy } from "../services/api";
import { useAuth } from "./AuthContext";

const ItineraryContext = createContext();

function getUserKey(user, key) {
  return user?.email ? `${user.email}_${key}` : `guest_${key}`;
}

function loadFromStorage(key) {
  try {
    const saved = localStorage.getItem(key);
    return saved ? JSON.parse(saved) : [];
  } catch {
    return [];
  }
}

function getTripId(trip) {
  return String(trip?._id || trip?.id || "");
}

function removeDuplicates(trips) {
  const seen = new Set();

  return trips.filter((trip) => {
    const id = getTripId(trip);
    if (!id || seen.has(id)) return false;
    seen.add(id);
    return true;
  });
}

export function ItineraryProvider({ children }) {
  const { user } = useAuth();

  const [myItineraries, setMyItineraries] = useState([]);
  const [favorites, setFavorites] = useState([]);

  useEffect(() => {
    if (!user) {
      setMyItineraries([]);
      setFavorites([]);
      return;
    }

    setMyItineraries(loadFromStorage(getUserKey(user, "myItineraries")));
    setFavorites(loadFromStorage(getUserKey(user, "favoritedItineraries")));
  }, [user]);

  useEffect(() => {
    if (!user) return;

    localStorage.setItem(
      getUserKey(user, "myItineraries"),
      JSON.stringify(myItineraries)
    );
  }, [myItineraries, user]);

  useEffect(() => {
    if (!user) return;

    localStorage.setItem(
      getUserKey(user, "favoritedItineraries"),
      JSON.stringify(favorites)
    );
  }, [favorites, user]);

  useEffect(() => {
    if (!user) return;

    async function fetchMyItineraries() {
      try {
        const response = await getItineraries();

        const storedTrips = loadFromStorage(getUserKey(user, "myItineraries"));
        const serverTrips = response.data || [];

    const userTrips = serverTrips.filter((trip) => {
      return (
        trip.userEmail === user.email ||
        trip.createdBy === user.email ||
        trip.ownerEmail === user.email
  );
});

setMyItineraries(removeDuplicates([...userTrips, ...storedTrips]));
      } catch (error) {
        console.error("Error loading itineraries:", error);
      }
    }

    fetchMyItineraries();
  }, [user]);

  const addItinerary = (itinerary) => {
    const tripId = itinerary._id || itinerary.id || crypto.randomUUID();

    const newTrip = {
      ...itinerary,
      id: tripId,
      userEmail: user?.email,
      createdBy: user?.email,
      ownerEmail: user?.email,
      isPublic: itinerary.isPublic ?? false,
      createdAt: itinerary.createdAt || new Date().toISOString(),
    };

    setMyItineraries((prev) => removeDuplicates([newTrip, ...prev]));
  };

  const updateItineraryInState = (updatedItinerary) => {
    const updatedId = getTripId(updatedItinerary);

    setMyItineraries((prev) =>
      prev.map((trip) => {
        const tripId = getTripId(trip);

        return tripId === updatedId
          ? {
              ...trip,
              ...updatedItinerary,
              id: trip.id || updatedItinerary.id,
              _id: trip._id || updatedItinerary._id,
              userEmail: trip.userEmail || user?.email,
              createdBy: trip.createdBy || user?.email,
              ownerEmail: trip.ownerEmail || user?.email,
            }
          : trip;
      })
    );
  };

  const togglePrivacy = async (id) => {
    const trip = myItineraries.find((item) => getTripId(item) === String(id));

    if (!trip) return;

    const newPrivacy = !trip.isPublic;

    try {
      const response = await updateItineraryPrivacy(id, newPrivacy);

      setMyItineraries((prev) =>
        prev.map((item) =>
          getTripId(item) === String(id)
            ? {
                ...response.data,
                userEmail: response.data.userEmail || user?.email,
                createdBy: response.data.createdBy || user?.email,
                ownerEmail: response.data.ownerEmail || user?.email,
              }
            : item
        )
      );
    } catch (error) {
      console.error("Error updating privacy:", error);
    }
  };

  const deleteItinerary = (id) => {
    setMyItineraries((prev) =>
      prev.filter((item) => getTripId(item) !== String(id))
    );

    setFavorites((prev) => prev.filter((item) => getTripId(item) !== String(id)));
  };

  const toggleFavorite = (itinerary) => {
    const tripId = itinerary._id || itinerary.id || crypto.randomUUID();

    setFavorites((prev) => {
      const exists = prev.some((f) => getTripId(f) === String(tripId));

      return exists
        ? prev.filter((f) => getTripId(f) !== String(tripId))
        : removeDuplicates([{ ...itinerary, id: itinerary.id || tripId }, ...prev]);
    });
  };

  const isFavorited = (id) =>
    favorites.some((f) => getTripId(f) === String(id));

  return (
    <ItineraryContext.Provider
      value={{
        myItineraries,
        addItinerary,
        updateItineraryInState,
        togglePrivacy,
        deleteItinerary,
        favorites,
        toggleFavorite,
        isFavorited,
      }}
    >
      {children}
    </ItineraryContext.Provider>
  );
}

export function useItineraries() {
  return useContext(ItineraryContext);
}