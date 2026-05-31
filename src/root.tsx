// @refresh reload
import { Suspense } from "solid-js";
import {
  Body,
  ErrorBoundary,
  FileRoutes,
  Head,
  Html,
  Link,
  Meta,
  Routes,
  Scripts,
  Title,
} from "solid-start";
import "./root.css";

export default function Root() {
  return (
    <Html lang="en">
      <Head>
        <Title>Valya AI</Title>
        <Meta charset="utf-8" />
        <Meta name="viewport" content="width=device-width, initial-scale=1" />
        <Meta name="theme-color" content="#0b1020" />
        <Meta
          name="description"
          content="Valya AI is an applied AI and automation studio — business and insurance-agency automation, native iOS and Windows apps, legal automation, and custom MCP servers."
        />
        <Link rel="icon" type="image/svg+xml" href="/vAI.svg" />
        <Link rel="icon" type="image/png" sizes="512x512" href="/vAI_512.png" />
        <Link rel="alternate icon" href="/favicon.ico" sizes="any" />
        <Link rel="apple-touch-icon" href="/apple-touch-icon.png" />
        <Link rel="canonical" href="https://valyaai.us/" />

        {/* Open Graph */}
        <Meta property="og:type" content="website" />
        <Meta property="og:site_name" content="Valya AI" />
        <Meta property="og:title" content="Valya AI — Applied AI & Automation Studio" />
        <Meta
          property="og:description"
          content="Business and insurance-agency automation, native iOS and Windows apps, legal automation, and custom MCP servers."
        />
        <Meta property="og:url" content="https://valyaai.us/" />
        <Meta property="og:image" content="https://valyaai.us/og-image.png" />
        <Meta property="og:image:type" content="image/png" />
        <Meta property="og:image:width" content="1200" />
        <Meta property="og:image:height" content="630" />

        {/* Twitter / X */}
        <Meta name="twitter:card" content="summary_large_image" />
        <Meta name="twitter:title" content="Valya AI — Applied AI & Automation Studio" />
        <Meta
          name="twitter:description"
          content="Business and insurance-agency automation, native iOS and Windows apps, legal automation, and custom MCP servers."
        />
        <Meta name="twitter:image" content="https://valyaai.us/og-image.png" />
      </Head>
      <Body>
        <Suspense>
          <ErrorBoundary>
            <Routes>
              <FileRoutes />
            </Routes>
          </ErrorBoundary>
        </Suspense>
        <Scripts />
      </Body>
    </Html>
  );
}
