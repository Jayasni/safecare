import {
  Stethoscope,
  HeartPulse,
  CalendarDays,
  Video,
  UserRound,
  ClipboardList,
} from "lucide-react";

function Services() {
  const services = [
    {
      icon: <Stethoscope />,
      title: "Doctor Consultation",
      description: "Find healthcare professionals and request consultations.",
    },
    {
      icon: <CalendarDays />,
      title: "Appointment Booking",
      description: "Schedule and manage your appointments conveniently.",
    },
    {
      icon: <Video />,
      title: "Online Consultation",
      description: "Connect with doctors through online consultations.",
    },
    {
      icon: <HeartPulse />,
      title: "Health Management",
      description: "Keep track of your healthcare journey.",
    },
    {
      icon: <UserRound />,
      title: "Patient Profiles",
      description: "Manage your personal healthcare information.",
    },
    {
      icon: <ClipboardList />,
      title: "Medical Records",
      description: "Organize your healthcare records securely.",
    },
  ];

  return (
    <main className="inner-page">
      <section className="inner-hero">
        <div className="container">
          <span className="eyebrow">OUR SERVICES</span>
          <h1>Healthcare services, made convenient.</h1>
          <p>
            Explore services designed to simplify
            your healthcare experience.
          </p>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <div className="service-grid">
            {services.map((service) => (
              <article className="service-card" key={service.title}>
                <div className="service-icon">
                  {service.icon}
                </div>

                <h3>{service.title}</h3>
                <p>{service.description}</p>
              </article>
            ))}
          </div>
        </div>
      </section>
    </main>
  );
}

export default Services;