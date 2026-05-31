import { Title, Meta } from "solid-start";

export default function Privacy() {
  return (
    <main class="page">
      <Title>Privacy Policy — Valya AI</Title>
      <Meta name="description" content="Privacy Policy for Valya AI (a DBA of Valya AI Corp)." />
      <Meta name="robots" content="index,follow" />

      <header class="subpage-header">
        <nav class="nav">
          <a class="brand" href="/">
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
          </a>
          <a class="nav-cta" href="/">
            ← Home
          </a>
        </nav>
      </header>

      <article class="legal">
        <p class="section-eyebrow">Legal</p>
        <h1 class="legal-title">Privacy Policy</h1>
        <p class="legal-meta">Last updated: May 31, 2026</p>

        <p>
          This Privacy Policy explains how <strong>Valya AI</strong>, a DBA of{" "}
          <strong>Valya AI Corp</strong> ("Valya AI," "we," "us," or "our"), collects,
          uses, and protects information in connection with our websites, applications, and
          services (collectively, the "Services"). By using our Services, you agree to the
          practices described here.
        </p>

        <h2>1. Information we collect</h2>
        <ul>
          <li>
            <strong>Information you provide.</strong> Such as your name, email address, and
            any details you submit when you contact us or request services.
          </li>
          <li>
            <strong>Business and client data.</strong> When we build or operate automation
            on your behalf, we may process data you authorize us to access (for example,
            records from systems you connect). We process this data only to provide the
            Services you've requested.
          </li>
          <li>
            <strong>Usage and device information.</strong> Standard technical data such as
            IP address, browser type, and pages viewed, collected to operate and secure
            the Services.
          </li>
        </ul>

        <h2>2. How we use information</h2>
        <ul>
          <li>To provide, maintain, and improve our Services;</li>
          <li>To respond to your inquiries and communicate with you;</li>
          <li>To build, operate, and support the automations and applications you request;</li>
          <li>To secure our Services and prevent fraud or abuse;</li>
          <li>To comply with legal obligations.</li>
        </ul>

        <h2>3. How we share information</h2>
        <p>
          We do <strong>not</strong> sell your personal information. We may share
          information with:
        </p>
        <ul>
          <li>
            <strong>Service providers and integrations</strong> that help us deliver the
            Services (for example, hosting, infrastructure, and the third-party platforms
            you ask us to connect, such as PostGrid, QuickBooks, or your chosen
            management systems), only as needed to perform their functions.
          </li>
          <li>
            <strong>AI model providers</strong> used to deliver AI features, limited to
            what is necessary to perform the requested task.
          </li>
          <li>
            <strong>Legal and safety</strong> recipients where required by law or to
            protect rights, safety, and property.
          </li>
        </ul>

        <h2>4. Data security</h2>
        <p>
          We use reasonable administrative, technical, and physical safeguards designed to
          protect information. No method of transmission or storage is completely secure,
          and we cannot guarantee absolute security.
        </p>

        <h2>5. Data retention</h2>
        <p>
          We retain information for as long as needed to provide the Services and for
          legitimate business or legal purposes. We delete or anonymize information when it
          is no longer required.
        </p>

        <h2>6. Your rights and choices</h2>
        <p>
          Depending on your location, you may have the right to access, correct, delete, or
          restrict the use of your personal information. To make a request, contact us at{" "}
          <a href="mailto:nate@valyaai.us">nate@valyaai.us</a>. You may also unsubscribe
          from non-essential communications at any time.
        </p>

        <h2>7. Children's privacy</h2>
        <p>
          Our Services are intended for businesses and individuals 18 and older. We do not
          knowingly collect personal information from children under 13.
        </p>

        <h2>8. Changes to this policy</h2>
        <p>
          We may update this Privacy Policy from time to time. When we do, we will revise
          the "Last updated" date above. Material changes will be communicated where
          appropriate.
        </p>

        <h2>9. Contact us</h2>
        <p>
          If you have questions about this Privacy Policy or our data practices, contact:
        </p>
        <p>
          <strong>Valya AI Corp</strong>
          <br />
          Attn: Nate Bingel
          <br />
          <a href="mailto:nate@valyaai.us">nate@valyaai.us</a>
        </p>
      </article>

      <footer class="footer">
        <nav class="footer-nav">
          <a href="/">Home</a>
          <a href="/about">About</a>
          <a href="mailto:nate@valyaai.us">Contact</a>
        </nav>
        <p>© {new Date().getFullYear()} Valya AI Corp. All rights reserved.</p>
        <p class="footer-sub">Valya AI is a DBA of Valya AI Corp</p>
      </footer>
    </main>
  );
}
