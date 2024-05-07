import { initializeApp } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-app.js";
import { getAuth, 
         GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.9.0/firebase-firestore.js";

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyABb9w7TrZuTsBKW-l-VvGoofSloIQxW3A",
  authDomain: "snapstock-2fa02.firebaseapp.com",
  projectId: "snapstock-2fa02",
  storageBucket: "snapstock-2fa02.appspot.com",
  messagingSenderId: "216913612232",
  appId: "1:216913612232:web:1fec4ae287e5df441744fd",
  measurementId: "G-GVMRB1JNLE"
};

  // Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const db = getFirestore(app);

export { auth, provider, db };