import { useState } from "react";
import { Mail, Phone, MapPin } from "lucide-react";

function Contact() {
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();

    setSubmitted(true);
  };

  return (
    <main className="inner-page">
      <section className="inner-hero">
        <div className="container">
          <span className="eyebrow">CONTACT US</span>
          <h1>We're here to help.</h1>
          <p>
            Have questions? Get in touch with our team.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container contact-grid">

          <div className="contact-details">
            <h2 className="section-heading">Let's connect</h2>

            <p className="section-description">
              Contact our support team for questions
              about the Healora platform.
            </p>

            <div className="contact-item">
              <Mail />
              <div>
                <strong>Email</strong>
                <p>support@healora.com</p>
              </div>
            </div>

            <div className="contact-item">
              <Phone />
              <div>
                <strong>Phone</strong>
                <p>+91 98765 43210</p>
              </div>
            </div>

            <div className="contact-item">
              <MapPin />
              <div>
                <strong>Location</strong>
                <p>Hyderabad, India</p>
              </div>
            </div>
          </div>

          <form className="auth-card" onSubmit={handleSubmit}>
            <h2>Send us a message</h2>

            <label htmlFor="contact-name">Full Name</label>
            <input id="contact-name" required placeholder="Enter your name" />

            <label htmlFor="contact-email">Email Address</label>
            <input id="contact-email" type="email" required placeholder="Enter email" />

            <label htmlFor="contact-message">Message</label>
            <textarea
              id="contact-message"
              required
              rows="5"
              placeholder="How can we help?"
            />

            <button type="submit" className="primary-btn">
              Send Message
            </button>

            {submitted && (
              <p className="form-notice">
                Your message form is ready. Contact API integration
                will be added in a later backend phase.
              </p>
            )}
          </form>

        </div>
      </section>
    </main>
  );
}

export default Contact;