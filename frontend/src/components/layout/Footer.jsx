import { Link } from "react-router-dom";
import {
  HeartPulse,
  Mail,
  Phone,
  MapPin,
} from "lucide-react";

function Footer() {
  return (
    <footer className="site-footer">
      <div className="container footer-grid">

        <div className="footer-brand">
          <Link to="/" className="brand">
            <HeartPulse size={27} />
            <span>Healora</span>
          </Link>

          <p>
            Your health deserves thoughtful care.
            Connect with trusted healthcare professionals
            and manage your appointments with ease.
          </p>
        </div>

        <div>
          <h3>Quick Links</h3>
          <Link to="/">Home</Link>
          <Link to="/about">About Us</Link>
          <Link to="/services">Services</Link>
          <Link to="/contact">Contact</Link>
        </div>

        <div>
          <h3>Account</h3>
          <Link to="/login">Login</Link>
          <Link to="/register">Register</Link>
        </div>

        <div>
          <h3>Contact Us</h3>

          <p><Mail size={16} /> support@healora.com</p>
          <p><Phone size={16} /> +91 98765 43210</p>
          <p><MapPin size={16} /> Hyderabad, India</p>
        </div>

      </div>

      <div className="container footer-bottom">
        <p>© 2026 Healora. All rights reserved.</p>
        <p>Healthcare, made simpler.</p>
      </div>
    </footer>
  );
}

export default Footer;