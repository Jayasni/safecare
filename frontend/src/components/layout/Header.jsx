import { useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { HeartPulse, Menu, X } from "lucide-react";

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const navItems = [
    { name: "Home", path: "/" },
    { name: "About", path: "/about" },
    { name: "Services", path: "/services" },
    { name: "Contact", path: "/contact" },
  ];

  return (
    <header className="site-header">
      <div className="container header-inner">

        <Link to="/" className="brand">
          <span className="brand-icon">
            <HeartPulse size={25} />
          </span>
          <span>Healora</span>
        </Link>

        <nav className={`nav-links ${menuOpen ? "open" : ""}`}>
          {navItems.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === "/"}
              onClick={() => setMenuOpen(false)}
              className={({ isActive }) =>
                isActive ? "nav-link active" : "nav-link"
              }
            >
              {item.name}
            </NavLink>
          ))}

          <div className="mobile-auth-links">
            <Link to="/login" onClick={() => setMenuOpen(false)}>
              Login
            </Link>

            <Link
              to="/register"
              className="primary-btn"
              onClick={() => setMenuOpen(false)}
            >
              Get Started
            </Link>
          </div>
        </nav>

        <div className="header-actions">
          <Link to="/login" className="login-link">
            Login
          </Link>

          <Link to="/register" className="primary-btn">
            Get Started
          </Link>
        </div>

        <button
          className="menu-toggle"
          onClick={() => setMenuOpen(!menuOpen)}
          aria-label="Toggle navigation"
          aria-expanded={menuOpen}
        >
          {menuOpen ? <X /> : <Menu />}
        </button>

      </div>
    </header>
  );
}

export default Header;