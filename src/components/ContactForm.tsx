import { createSignal } from "solid-js";

const CONTACT_EMAIL = "nate@valyaai.us";

export default function ContactForm() {
  const [name, setName] = createSignal("");
  const [email, setEmail] = createSignal("");
  const [message, setMessage] = createSignal("");

  function handleSubmit(e: Event) {
    e.preventDefault();
    const subject = `New inquiry from ${name() || "the Valya AI site"}`;
    const body =
      `Name: ${name()}\n` +
      `Email: ${email()}\n\n` +
      `${message()}`;
    const href =
      `mailto:${CONTACT_EMAIL}` +
      `?subject=${encodeURIComponent(subject)}` +
      `&body=${encodeURIComponent(body)}`;
    window.location.href = href;
  }

  return (
    <form class="contact-form" onSubmit={handleSubmit}>
      <div class="field">
        <label for="cf-name">Name</label>
        <input
          id="cf-name"
          type="text"
          name="name"
          required
          autocomplete="name"
          value={name()}
          onInput={(e) => setName(e.currentTarget.value)}
          placeholder="Your name"
        />
      </div>
      <div class="field">
        <label for="cf-email">Email</label>
        <input
          id="cf-email"
          type="email"
          name="email"
          required
          autocomplete="email"
          value={email()}
          onInput={(e) => setEmail(e.currentTarget.value)}
          placeholder="you@example.com"
        />
      </div>
      <div class="field">
        <label for="cf-message">Message</label>
        <textarea
          id="cf-message"
          name="message"
          rows={5}
          required
          value={message()}
          onInput={(e) => setMessage(e.currentTarget.value)}
          placeholder="Tell us a bit about your project…"
        />
      </div>
      <button class="btn btn-primary contact-submit" type="submit">
        Send message
      </button>
      <p class="contact-form-note">
        This opens your email app pre-filled to {CONTACT_EMAIL}.
      </p>
    </form>
  );
}
