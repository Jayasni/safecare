import { HeartPulse, ShieldCheck, Users, Target } from "lucide-react";

function About() {
  return (
    <main className="inner-page">
      <section className="inner-hero">
        <div className="container">
          <span className="eyebrow">ABOUT HEALORA</span>
          <h1>Healthcare that puts people first.</h1>
          <p>
            Our goal is to make healthcare access
            simpler, more convenient and patient-focused.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container about-grid">
          <div>
            <span className="eyebrow">OUR MISSION</span>
            <h2 className="section-heading">
              Connecting people with better healthcare.
            </h2>
            <p className="section-description">
              Healora is designed to bring patients and
              healthcare professionals together through
              a simple appointment management experience.
            </p>
          </div>

          <div className="about-cards">
            <div className="about-card">
              <HeartPulse />
              <h3>Patient First</h3>
              <p>Making patient experience our priority.</p>
            </div>

            <div className="about-card">
              <ShieldCheck />
              <h3>Trust & Security</h3>
              <p>Building a secure healthcare experience.</p>
            </div>

            <div className="about-card">
              <Users />
              <h3>Accessibility</h3>
              <p>Making healthcare services easier to access.</p>
            </div>

            <div className="about-card">
              <Target />
              <h3>Our Vision</h3>
              <p>Making healthcare management simpler.</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}

export default About;