import { useState } from "react";
import { Link } from "react-router-dom";
import { HeartPulse, LockKeyhole } from "lucide-react";

function Login() {
  const [message, setMessage] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    setMessage(
      "Login interface is ready. Backend authentication will be connected in Phase 6."
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
          <h2>Welcome Back!</h2>
          <p>Login to continue your healthcare journey.</p>
        </div>

        <form onSubmit={handleSubmit}>

          <label htmlFor="login-email">Email Address</label>
          <input
            id="login-email"
            type="email"
            placeholder="Enter your email"
            required
          />

          <label htmlFor="login-password">Password</label>
          <input
            id="login-password"
            type="password"
            placeholder="Enter your password"
            required
          />

          <button type="submit" className="primary-btn auth-submit">
            <LockKeyhole size={18} />
            Login
          </button>

        </form>

        {message && <p className="form-notice">{message}</p>}

        <p className="auth-switch">
          Don't have an account?
          <Link to="/register"> Create Account</Link>
        </p>

      </div>
    </main>
  );
}

export default Login;