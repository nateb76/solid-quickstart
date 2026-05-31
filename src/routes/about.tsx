import { Title, Meta } from "solid-start";

export default function About() {
  return (
    <main class="page">
      <Title>About — Valya AI</Title>
      <Meta
        name="description"
        content="Valya AI is an applied AI and automation studio building business and insurance-agency automation, native iOS and Windows apps, legal automation, and custom MCP servers."
      />

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
        <p class="section-eyebrow">About</p>
        <h1 class="legal-title">About Valya AI</h1>

        <p>
          <strong>Valya AI</strong> is an applied artificial-intelligence and automation
          studio. We design and build software that removes manual, repetitive work — so
          businesses and independent professionals can spend their time on the work that
          actually moves things forward.
        </p>

        <h2>What we do</h2>
        <p>
          We build end-to-end automation and native applications across the platforms our
          clients already rely on. Our work spans:
        </p>
        <ul>
          <li>
            <strong>Business automation</strong> — connecting tools, data, and workflows,
            including AI-powered Claude connectors and bookkeeping automation for
            QuickBooks.
          </li>
          <li>
            <strong>Native apps</strong> — App Store–ready iOS applications and desktop
            applications for Windows.
          </li>
          <li>
            <strong>Insurance-agency automation</strong> — policy-data import, ACORD and
            supplemental form auto-fill, certificate-of-insurance compliance, and secure
            carrier-portal automation.
          </li>
          <li>
            <strong>Legal services automation</strong> — pre-litigation workflows such as
            demand-letter generation, document assembly, and deadline tracking.
          </li>
          <li>
            <strong>Mail automation</strong> — programmatic physical and digital mail
            powered by PostGrid.
          </li>
          <li>
            <strong>Custom MCP servers</strong> — bespoke Model Context Protocol
            integrations that securely connect AI assistants to your tools and data.
          </li>
        </ul>

        <h2>How we work</h2>
        <p>
          We pair frontier AI models with practical engineering: clear scoping, secure
          integrations, and software that's built to be maintained. Whether the goal is a
          single automation or a full application, we focus on reliability, data security,
          and a result that fits the way you already operate.
        </p>

        <h2>Company</h2>
        <p>
          Valya AI is a DBA of <strong>Valya AI Corp</strong>. The company is led by
          founder <strong>Nate Bingel</strong>.
        </p>

        <h2>Get in touch</h2>
        <p>
          For new projects, partnerships, or questions, reach us at{" "}
          <a href="mailto:nate@valyaai.us">nate@valyaai.us</a>.
        </p>
      </article>

      <footer class="footer">
        <nav class="footer-nav">
          <a href="/">Home</a>
          <a href="/privacy">Privacy Policy</a>
          <a href="mailto:nate@valyaai.us">Contact</a>
        </nav>
        <p>© {new Date().getFullYear()} Valya AI Corp. All rights reserved.</p>
        <p class="footer-sub">Valya AI is a DBA of Valya AI Corp</p>
      </footer>
    </main>
  );
}
