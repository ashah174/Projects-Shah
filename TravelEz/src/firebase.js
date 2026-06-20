import { initializeApp } from "firebase/app";
import { getAuth, GoogleAuthProvider } from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyDpDyTWD9FOEIAIO5VtLxWMPLzdG93YFSk",
  authDomain: "travelez-1292b.firebaseapp.com",
  projectId: "travelez-1292b",
  storageBucket: "travelez-1292b.firebasestorage.app",
  messagingSenderId: "10760241629959",
  appId: "1:10760241629959:web:ebcfc27088193df9c14efa",
  measurementId: "G-KCMMDWRHLL",
};

const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
