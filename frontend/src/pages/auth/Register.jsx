import { useState } from "react";
import { Link } from "react-router-dom";
import { HeartPulse, UserPlus } from "lucide-react";

function Register() {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    setMessage(
      "Registration interface is ready. Account creation will be connected to the backend in Phase 6."
    );
  };

  return (
    <main className="auth-page">
      <div className="auth-card">

        <div className="auth-logo">
          <HeartPulse size={35} />
          <h1>Healora</h1>
        </div>

        <div className="auth-heading">
          <h2>Create Your Account</h2>
          <p>Join Healora for a simpler healthcare experience.</p>
        </div>

        <form onSubmit={handleSubmit}>

          <label htmlFor="register-name">Full Name</label>
          <input
            id="register-name"
            type="text"
            placeholder="Enter your full name"
            required
          />

          <label htmlFor="register-email">Email Address</label>
          <input
            id="register-email"
            type="email"
            placeholder="Enter your email"
            required
          />

          <label htmlFor="register-phone">Phone Number</label>
          <input
            id="register-phone"
            type="tel"
            placeholder="Enter your phone number"
            pattern="[0-9]{10}"
            required
          />

          <label htmlFor="register-password">Password</label>
          <input
            id="register-password"
            type="password"
            placeholder="Create a password"
            minLength="8"
            required
          />

          <label htmlFor="register-confirm">Confirm Password</label>
          <input
            id="register-confirm"
            type="password"
            placeholder="Confirm your password"
            minLength="8"
            required
          />

          <button type="submit" className="primary-btn auth-submit">
            <UserPlus size={18} />
            Create Account
          </button>

        </form>

        {message && <p className="form-notice">{message}</p>}

        <p className="auth-switch">
          Already have an account?
          <Link to="/login"> Login</Link>
        </p>

      </div>
    </main>
  );
}

export default Register;