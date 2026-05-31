import { Title } from "solid-start";
import { HttpStatusCode } from "solid-start/server";

export default function NotFound() {
  return (
    <main class="page">
      <Title>Page Not Found — Valya AI</Title>
      <HttpStatusCode code={404} />

      <header class="subpage-header">
        <nav class="nav">
          <a class="brand" href="/">
            <img
              class="brand-logo"
              src="/vAI.svg"
              alt="Valya AI logo"
              width="32"
              height="32"
            />
            <span class="brand-mark" style="display:none">V</span> Valya&nbsp;AI
          </a>
          <a class="nav-cta" href="/">
            ← Home
          </a>
        </nav>
      </header>

      <section class="notfound">
        <p class="notfound-code">404</p>
        <h1 class="notfound-title">Page not found</h1>
        <p class="notfound-sub">
          The page you're looking for doesn't exist or may have moved.
        </p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="/">
            Back to home
          </a>
          <a class="btn btn-ghost" href="mailto:nate@valyaai.us">
            Contact us
          </a>
        </div>
      </section>
    </main>
  );
}
