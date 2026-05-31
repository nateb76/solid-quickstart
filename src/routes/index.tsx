import { Title, Meta } from "solid-start";
import ContactForm from "~/components/ContactForm";

const services = [
  {
    icon: "⚙️",
    title: "Business Automation Apps",
    blurb:
      "Custom workflow automation that removes manual busywork — intake, routing, reporting, and back-office operations wired together so your team can focus on the work that matters. Includes ready-to-use Claude connectors that bring AI directly into your existing tools and processes.",
  },
  {
    icon: "📊",
    title: "Bookkeeping Automation for QuickBooks",
    blurb:
      "Hands-off bookkeeping that syncs with QuickBooks — automated transaction categorization, invoice and payment tracking, reconciliation, and reporting, so your books stay clean and current without the manual entry.",
  },
  {
    icon: "✉️",
    title: "Mail Apps via PostGrid",
    blurb:
      "Programmatic physical and digital mail powered by the PostGrid platform. Trigger letters, postcards, and certified mail directly from your software — fully tracked and verifiable.",
  },
  {
    icon: "📱",
    title: "iOS Apps",
    blurb:
      "Native, App Store–ready iOS applications built to Apple's Human Interface Guidelines — fast, accessible, and designed to feel right at home on iPhone and iPad.",
  },
  {
    icon: "🪟",
    title: "Windows Apps",
    blurb:
      "Reliable desktop applications for Windows that bring automation and AI to the platform your business already runs on, with clean installs and smooth updates.",
  },
  {
    icon: "⚖️",
    title: "Legal Services — Pre-Litigation Automation",
    blurb:
      "Automated pre-litigation workflows: demand letters, document assembly, deadline tracking, and structured case intake — accelerating the steps that happen before a matter ever reaches court.",
  },
  {
    icon: "🔌",
    title: "Custom MCPs",
    blurb:
      "Bespoke Model Context Protocol servers that securely connect AI assistants to your tools, data, and APIs — turning your internal systems into capabilities an AI can use.",
  },
  {
    icon: "🛡️",
    title: "Insurance Agency Automation",
    blurb:
      "Purpose-built automation for independent agents: consumer-permissioned policy import, dec-page extraction, and two-way sync across agency management systems and CRMs like AgencyZoom, EZLynx, HawkSoft, and Momentum.",
  },
  {
    icon: "📝",
    title: "ACORD & Supplemental Auto-Fill",
    blurb:
      "Enter client and risk data once and auto-populate ACORD forms and carrier supplementals across the board — with cross-field validation and e-sign, eliminating duplicate data entry on commercial applications.",
  },
  {
    icon: "📜",
    title: "Certificate of Insurance (COI) Compliance",
    blurb:
      "Automated certificate issuance, tracking, and verification — AI reads policy language for coverage gaps and keeps compliance communications flowing to the right parties in real time.",
  },
  {
    icon: "🌐",
    title: "Carrier Portal Automation",
    blurb:
      "When a carrier has no public API, our secure browser-agent layer drives the portal for you — pulling renewals, books of business, and policy data, then routing it downstream to quoting, mail, and CRM.",
  },
  {
    icon: "📞",
    title: "AI Voice & Communication Agents",
    blurb:
      "AI-powered phone, SMS, and intake agents that handle renewals, reminders, and first-touch client conversations — integrated with your phone system, CRM, and direct-mail workflows.",
  },
];

export default function Home() {
  return (
    <main class="page">
      <Title>Valya AI — Intelligent Automation, iOS & Windows Apps, Custom MCPs</Title>
      <Meta
        name="description"
        content="Valya AI builds business and insurance-agency automation, PostGrid-powered mail apps, native iOS and Windows applications, ACORD form auto-fill, pre-litigation legal automation, and custom MCP servers."
      />

      <header class="hero">
        <nav class="nav">
          <span class="brand">
            <img
              class="brand-logo"
              src="/vAI.svg"
              alt="Valya AI logo"
              width="32"
              height="32"
              onError={(e) => {
                const img = e.currentTarget;
                img.style.display = "none";
                const fallback = img.nextElementSibling as HTMLElement | null;
                if (fallback) fallback.style.display = "inline-flex";
              }}
            />
            <span class="brand-mark" style="display:none">V</span> Valya&nbsp;AI
          </span>
          <a class="nav-cta" href="#contact">
            Contact
          </a>
        </nav>

        <div class="hero-inner">
          <p class="eyebrow">Applied AI &amp; Automation Studio</p>
          <h1 class="hero-title">
            Intelligent software that does the <span class="grad">busywork</span> for you.
          </h1>
          <p class="hero-sub">
            Valya AI designs and ships automation platforms, native apps, and custom AI
            integrations for businesses and insurance agencies — from the App Store to
            the back office.
          </p>
          <div class="hero-actions">
            <a class="btn btn-primary" href="#services">
              Explore services
            </a>
            <a class="btn btn-ghost" href="#contact">
              Get in touch
            </a>
          </div>
        </div>
      </header>

      <section id="services" class="section">
        <p class="section-eyebrow">What we build</p>
        <h2 class="section-title">Services</h2>
        <div class="grid">
          {services.map((s) => (
            <article class="card">
              <div class="card-icon" aria-hidden="true">
                {s.icon}
              </div>
              <h3 class="card-title">{s.title}</h3>
              <p class="card-blurb">{s.blurb}</p>
            </article>
          ))}
        </div>
      </section>

      <section class="section section-band">
        <div class="band-inner">
          <h2 class="band-title">Built for the platforms your business lives on.</h2>
          <p class="band-sub">
            Apple, Windows, and the web — connected by AI and automation that works the
            way you do.
          </p>
        </div>
      </section>

      <section id="contact" class="section contact">
        <p class="section-eyebrow">Let's talk</p>
        <h2 class="section-title">Contact</h2>
        <p class="contact-lead">
          Have a project in mind or want to learn more about what Valya AI can do for you?
          Reach out directly.
        </p>
        <div class="contact-grid">
          <div class="contact-card">
            <p class="contact-name">Nate Bingel</p>
            <p class="contact-role">Founder, Valya AI</p>
            <a class="contact-email" href="mailto:nate@valyaai.us">
              nate@valyaai.us
            </a>
          </div>
          <ContactForm />
        </div>
      </section>

      <footer class="footer">
        <nav class="footer-nav">
          <a href="/about">About</a>
          <a href="/privacy">Privacy Policy</a>
          <a href="mailto:nate@valyaai.us">Contact</a>
        </nav>
        <p>© {new Date().getFullYear()} Valya AI Corp. All rights reserved.</p>
        <p class="footer-sub">Valya AI is a DBA of Valya AI Corp</p>
        <p class="footer-sub">Insurance &amp; business automation · iOS &amp; Windows apps · Legal automation · Custom MCPs</p>
      </footer>
    </main>
  );
}
