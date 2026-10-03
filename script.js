import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
  signOut,
  onAuthStateChanged 
} from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// Complete Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyCf_NZ7EWHWEUt8OIrcHMAu0ffmSLNx_5s",
  authDomain: "nexoraauth-f1692.firebaseapp.com",
  projectId: "nexoraauth-f1692",
  storageBucket: "nexoraauth-f1692.firebasestorage.app",
  messagingSenderId: "222499366415",
  appId: "1:222499366415:web:958bd87b357cf8b77d657a",
  measurementId: "G-TX7N006I"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

// Get HTML Elements
const emailInput = document.getElementById('email-input');
const passwordInput = document.getElementById('password-input');
const loginBtn = document.getElementById('login-btn');
const signupBtn = document.getElementById('signup-btn');
const authStatus = document.getElementById('auth-status');

// Sign Up
if (signupBtn) {
  signupBtn.addEventListener('click', async () => {
    try {
      await createUserWithEmailAndPassword(auth, emailInput.value, passwordInput.value);
      authStatus.textContent = "Account created successfully!";
      authStatus.style.color = "green";
    } catch (error) {
      authStatus.textContent = error.message;
      authStatus.style.color = "red";
    }
  });
}

// Log In
if (loginBtn) {
  loginBtn.addEventListener('click', async () => {
    try {
      await signInWithEmailAndPassword(auth, emailInput.value, passwordInput.value);
      authStatus.textContent = "Logged in successfully!";
      authStatus.style.color = "green";
    } catch (error) {
      authStatus.textContent = error.message;
      authStatus.style.color = "red";
    }
  });
}

// Auth State Observer (Updates the UI when logged in)
onAuthStateChanged(auth, (user) => {
  if (user) {
    authStatus.innerHTML = `Welcome! You are logged in as: <strong>${user.email}</strong>`;
    authStatus.style.color = "green";
  } else {
    authStatus.textContent = "Please sign up or log in.";
    authStatus.style.color = "#333";
  }
});
