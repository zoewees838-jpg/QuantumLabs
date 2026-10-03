import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { 
  getAuth, 
  createUserWithEmailAndPassword, 
  signInWithEmailAndPassword, 
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

// Helper function to resolve GitHub Pages subfolder paths automatically
function goToDashboard() {
  const currentPath = window.location.pathname;
  const directory = currentPath.substring(0, currentPath.lastIndexOf('/'));
  window.location.href = `${window.location.origin}${directory}/dashboard.html`;
}

// Sign Up
if (signupBtn) {
  signupBtn.addEventListener('click', async (e) => {
    e.preventDefault(); // Prevents instant page reload if inside an HTML form
    try {
      await createUserWithEmailAndPassword(auth, emailInput.value, passwordInput.value);
      authStatus.textContent = "Account created! Redirecting...";
      authStatus.style.color = "green";
      goToDashboard();
    } catch (error) {
      authStatus.textContent = error.message;
      authStatus.style.color = "red";
    }
  });
}

// Log In
if (loginBtn) {
  loginBtn.addEventListener('click', async (e) => {
    e.preventDefault(); // Prevents instant page reload if inside an HTML form
    try {
      await signInWithEmailAndPassword(auth, emailInput.value, passwordInput.value);
      authStatus.textContent = "Logged in! Redirecting...";
      authStatus.style.color = "green";
      goToDashboard();
    } catch (error) {
      authStatus.textContent = error.message;
      authStatus.style.color = "red";
    }
  });
}

// Auth State Observer - Redirects automatically if already logged in
onAuthStateChanged(auth, (user) => {
  if (user && !window.location.pathname.endsWith('dashboard.html')) {
    goToDashboard();
  }
});
