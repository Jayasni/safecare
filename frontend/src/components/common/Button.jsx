import { Link } from "react-router-dom";

function Button({
  children,
  to,
  variant = "primary",
  type = "button",
  onClick,
}) {
  const className =
    variant === "secondary"
      ? "secondary-btn"
      : "primary-btn";

  if (to) {
    return (
      <Link to={to} className={className}>
        {children}
      </Link>
    );
  }

  return (
    <button
      type={type}
      className={className}
      onClick={onClick}
    >
      {children}
    </button>
  );
}

export default Button;