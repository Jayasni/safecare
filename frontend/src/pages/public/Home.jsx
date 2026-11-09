import {
  ArrowRight,
  CalendarCheck,
  Clock,
  HeartPulse,
  ShieldCheck,
  Stethoscope,
  UserRoundCheck,
  Video,
} from "lucide-react";

import Button from "../../components/common/Button";

function Home() {
  const services = [
    {
      icon: <Stethoscope size={27} />,
      title: "Expert Doctors",
      description:
        "Connect with experienced healthcare professionals.",
    },
    {
      icon: <CalendarCheck size={27} />,
      title: "Easy Appointments",
      description:
        "Book appointments according to your schedule.",
    },
    {
      icon: <Video size={27} />,
      title: "Online Consultation",
      description:
        "Access healthcare professionals remotely.",
    },
  ];

  const features = [
    "Simple appointment scheduling",
    "Trusted healthcare professionals",
    "Secure patient information",
    "Convenient appointment management",
  ];

  return (
    <main>

      {/* HERO SECTION */}

      <section className="hero-section">
        <div className="container hero-grid">

          <div className="hero-content">

            <span className="eyebrow">
              <HeartPulse size={17} />
              Your Health, Our Priority
            </span>

            <h1>
              Better Healthcare
              <br />
              Starts With <span>Better Care.</span>
            </h1>

            <p>
              Experience a simpler way to manage your healthcare.
              Discover trusted doctors, schedule appointments
              and take control of your wellbeing.
            </p>

            <div className="hero-actions">
              <Button to="/register">
                Book an Appointment
                <ArrowRight size={18} />
              </Button>

              <Button to="/services" variant="secondary">
                Explore Services
              </Button>
            </div>

            <div className="hero-trust">
              <ShieldCheck size={19} />
              <span>Patient-focused and secure healthcare experience</span>
            </div>

          </div>

          <div className="hero-visual">

            <div className="hero-image-placeholder">
              <div className="medical-symbol">
                <HeartPulse size={85} />
              </div>
              <span>Care that puts you first</span>
            </div>

            <div className="floating-card">
              <CalendarCheck size={25} />
              <div>
                <strong>Easy Booking</strong>
                <small>Appointments made simple</small>
              </div>
            </div>

          </div>

        </div>
      </section>

      {/* SERVICES SECTION */}

      <section className="section services-section">
        <div className="container">

          <div className="section-intro">
            <span className="eyebrow">OUR SERVICES</span>

            <h2 className="section-heading">
              Healthcare designed around you
            </h2>

            <p className="section-description">
              Everything you need for a more convenient
              healthcare experience.
            </p>
          </div>

          <div className="service-grid">
            {services.map((service) => (
              <article className="service-card" key={service.title}>
                <div className="service-icon">
                  {service.icon}
                </div>

                <h3>{service.title}</h3>

                <p>{service.description}</p>

                <Button to="/services" variant="secondary">
                  Learn More <ArrowRight size={16} />
                </Button>
              </article>
            ))}
          </div>

        </div>
      </section>

      {/* WHY CHOOSE US */}

      <section className="section why-section">
        <div className="container why-grid">

          <div className="why-visual">
            <div className="why-icon">
              <UserRoundCheck size={75} />
            </div>
            <div className="why-caption">
              <HeartPulse size={21} />
              Thoughtful care, every step of the way
            </div>
          </div>

          <div className="why-content">

            <span className="eyebrow">WHY HEALORA</span>

            <h2 className="section-heading">
              Making your healthcare journey easier
            </h2>

            <p className="section-description">
              We bring healthcare services and appointment
              management together in one convenient platform.
            </p>

            <div className="feature-list">
              {features.map((feature) => (
                <div className="feature-item" key={feature}>
                  <ShieldCheck size={20} />
                  <span>{feature}</span>
                </div>
              ))}
            </div>

            <Button to="/about">
              Discover Healora <ArrowRight size={18} />
            </Button>

          </div>

        </div>
      </section>

      {/* CTA */}

      <section className="section cta-section">
        <div className="container cta-content">
          <Clock size={36} />

          <h2>Ready to take the next step in your healthcare?</h2>

          <p>
            Create your account and start managing
            your appointments with Healora.
          </p>

          <Button to="/register">
            Get Started <ArrowRight size={18} />
          </Button>
        </div>
      </section>

    </main>
  );
}

export default Home;