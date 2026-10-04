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

// MANUAL PAYMENT FLOW & AUTOMATED AI PROFIT ENGINE
function triggerStarterSubscription() {
  const accountDetails = `
========================================
       NEXORA PAYMENT DETAILS
========================================
Bank Name:     Moniepoint MFB / Wema Bank
Account Name:  Nexora Global / Loretta
Account No:    0123456789
Amount:        ₦3,000.00
Reference:     NX-ACT-LORETTA
========================================

Please transfer exactly ₦3,000 to the account above.
After payment, click OK to confirm your transfer.
  `;

  if (confirm(accountDetails)) {
    const confirmPayment = confirm("Have you sent the ₦3,000 payment to the account above?");
    
    if (confirmPayment) {
      alert("Payment submitted! Your account activation is processing.");

      isSubscribed = true;
      walletBalance = 3000.00;
      availableCash = 3000.00;

      document.getElementById('total-balance').innerText = "₦3,000.00";
      document.getElementById('available-balance').innerText = "₦3,000.00";
      document.getElementById('balance-sub').innerText = "+Account Activated & Compounding";
      if (document.getElementById('activation-banner')) {
        document.getElementById('activation-banner').style.display = "none";
      }

      const row = `<tr>
        <td>#TX-30001</td>
        <td>Bank Deposit (Starter)</td>
        <td>₦3,000.00</td>
        <td>Just now</td>
        <td><span class="status-tag active">Verified</span></td>
      </tr>`;
      if (document.getElementById('transaction-rows')) {
        document.getElementById('transaction-rows').innerHTML = row + document.getElementById('transaction-rows').innerHTML;
      }

      startAIProfitEngine();
    }
  }
}

function startAIProfitEngine() {
  alert("AI Automated Yield Engine Started! Your profits will now compound automatically.");

  setInterval(() => {
    const profitIncrement = 15.50; 
    
    walletBalance += profitIncrement;
    investedAmount += profitIncrement;

    if (document.getElementById('total-balance')) {
      document.getElementById('total-balance').innerText = `₦${walletBalance.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    }
    if (document.getElementById('invested-balance')) {
      document.getElementById('invested-balance').innerText = `₦${investedAmount.toLocaleString('en-US', {minimumFractionDigits: 2})}`;
    }
    if (document.getElementById('balance-sub')) {
      document.getElementById('balance-sub').innerText = `+AI Active Yield (+₦${profitIncrement}/cycle)`;
    }
  }, 10000); // Increments every 10 seconds
}

