# Insurance & Automation Software for Independent Agents — Zapier & API Connectivity

A reference of platforms independent agents (and an automation shop like Valya AI) use, scored on how they connect to automation tooling. Verified May 2026.

## Connection legend

- **Native Zapier** — Its own published Zapier app (triggers/actions, no code).
- **API** — Documented REST API you call directly (from Replit middleware or a Zapier Webhooks/Code step).
- **Partner API** — Connects only through a vendor partner program (no public Zapier app).
- **IVANS** — Carrier policy data flows in via IVANS download, not a general automation API.
- **Portal / agent** — No public API; reach it with browser automation (CoWork / Claude-for-Chrome skill). This is the Farmers-portal pattern.

-----

## Tier 1 — Insurance data & policy-import APIs ("Plaid for insurance")

| Platform | What it does | Connects via | Notes / links |
|---|---|---|---|
| **Canopy Connect** | 1-click consumer-permissioned pull of dec pages, coverages, drivers, vehicles, claims from 400+ carriers | Native Zapier + API + webhooks | Strongest fit for your stack. usecanopy.com/api · zapier.com/apps/canopy-connect |
| **InsurGrid** | Policy data collection + dec-page extraction; pushes to AMS/CRM/raters | Native Zapier + API | Integrates HawkSoft, EZLynx, AgencyZoom, TurboRater |
| **Fenris** | Identity + risk data prefill (auto-fills applicant/risk fields) | API | Used by EZLynx for prefill; developer API for embedding |
| **RiskAdvisor** | Standardizes client intake before it hits the AMS | Partner API | HawkSoft partner; branded digital forms + PolicyLink |

-----

## Tier 2 — Agency Management Systems (AMS)

| Platform | What it does | Connects via | Notes / links |
|---|---|---|---|
| **EZLynx** | AMS + rating engine; most automation-friendly AMS | Native Zapier + API | Triggers: new/modified applicant, prospect, document, note, opportunity. ezlynx.com/products/ezlynx-api-solutions |
| **Momentum AMP** (was NowCerts) | Affordable cloud AMS; strong COI / additional-insured tracking | API (+ limited Zapier) | Open API at api.nowcerts.com; public Zapier app thin on policy/contact data |
| **HawkSoft** | Popular small/mid-agency AMS | Partner API (2-way write-back) | No native Zapier app — connect via API partners (InsurGrid, InsuredMine, Levitate) |
| **Vertafore AMS360** | Enterprise AMS | IVANS + Partner API | Integrates PL Rating, TurboRater. No native Zapier app |
| **Applied Epic** | Enterprise AMS (standard at scale) | IVANS + Partner API | 450+ IVANS integrations; Applied Developer program; ecosystem incl. Indio, CSR24 |
| **QQ Catalyst** | Vertafore AMS for smaller agencies | IVANS + Partner API | Reach via partners (XILO, InsuredMine, GloveBox) |
| **Jenesis / AgencyBloc** | Small-agency AMS / life-&-health agency mgmt | Partner API | Niche; verify current API status before building |

-----

## Tier 3 — Insurance CRM / sales & service automation

| Platform | What it does | Connects via | Notes / links |
|---|---|---|---|
| **AgencyZoom** | P&C sales pipeline, service center, automation (your CRM) | Native Zapier + API | Connect with API key + secret. Triggers: new lead, status change, new/updated service request. Now Vertafore-owned |
| **Better Agency** | Insurance CRM with 100+ automation templates | Native Zapier (no API) | Owned by GloveBox since Dec 2024; integrates IVANS, Momentum, Twilio, Thanks.io |
| **InsuredMine** | Insurance CRM + analytics; deep AMS sync | Native Zapier + 2-way API | Syncs HawkSoft, AMS360, Epic, Momentum, EZLynx + raters |

-----

## Tier 4 — Comparative raters & quoting

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **EZLynx Rating** | Personal + commercial comparative rater | API (within EZLynx) | Feeds rating data to proposal tools |
| **Tarmika** (Applied) | Single-entry commercial quoting | Carrier API + AMS | ~31 carriers; best for Applied Epic / EZLynx shops |
| **Semsee** | Small-commercial BOP/GL quoting | Carrier API + RPA | ~48 carriers; free Essential tier |
| **Bold Penguin** | Commercial quote/bind + lead Exchange | Carrier API | 45+ carriers; secure carrier API |
| **CoverForce** | Commercial quoting infrastructure | Developer API | Best if you want to embed quoting in your own app |
| **Appulate** | Submission management / routing to underwriters | Partner API | Workflow-focused vs instant quotes |
| **PL Rating** (Vertafore) | Personal lines comparative rater | AMS integration | Workstation install; integrates AMS360 |
| **TurboRater / QuoteRush** | Personal lines raters | Partner API | Common InsurGrid/InsuredMine handoff targets |

> Most commercial raters expose *carrier-side* APIs, so agent-side Zapier automation is limited. CoverForce and Bold Penguin are the most developer-friendly to build on.

-----

## Tier 5 — ACORD forms & commercial application automation (auto-fill supplementals)

This is your "fill out the supplementals automatically" tier.

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **Indio** (Applied) | Smart-form auto-mapping across ACORD forms + huge digitized library of carrier **supplementals**, questionnaires, e-sign; TurboTax-style intake | Within Applied ecosystem (AMS360/Epic import-export) | The category leader for ACORD + supplemental auto-fill. Enter once, auto-populates across forms |
| **Herald** | Single **API** that normalizes carrier questions and quotes/binds commercial across many carriers; auto-fills applicant profiles | Developer API | Built for devs/AI agents — ideal Valya AI building block. heraldapi.com |
| **Tarmika** | Single entry → multiple carrier apps/supplementals | Carrier API + AMS | (Also in Tier 4) |
| **Instafill.ai** | AI auto-fills ACORD PDFs (125, 140, etc.) with cross-field validation | API / web app | Good for one-off or SMB-facing form fill |
| **EasyApps** (Agency Software) | 800+ ACORD form filler with client/cert database | Desktop | Legacy but exhaustive form coverage |

-----

## Tier 6 — COI / certificate-of-insurance compliance

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **myCOI** | COI tracking + issuance; agent-side broker workflows | Pre-built integrations + API | Automated compliance comms to accounting/PM tools |
| **TrustLayer** | AI-powered COI extraction + verification | API (Developers program) | Strong Procore integration; configurable rules |
| **Certificial** | Real-time policy monitoring ("Smart COI") | API | Source-verified data vs static PDFs |
| **Jones / BCS (RiskBot)** | COI tracking for GCs / property | API / partner | RiskBot reads policy language for gaps |

-----

## Tier 7 — Client portals & relationship marketing

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **GloveBox** | Agency-branded client portal + mobile app | API + Zapier + Twilio | Integrates Applied Epic, AMS360, HawkSoft, EZLynx API, Momentum, QQ Catalyst |
| **Levitate** | Relationship/email marketing with AI | API / AMS integrations | 2-way write-back to HawkSoft |
| **Agency Revolution** | Insurance email marketing automation | AMS integrations | Syncs with AMS customer data |
| **Thanks.io** | Handwritten cards / direct mail automation | Native Zapier + API | Common AgencyZoom/Better Agency add-on |

-----

## Tier 8 — Online intake / digital applications

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **XILO** | Online quote forms + intake automation | Native Zapier + API | Integrates EZLynx, HawkSoft, AMS360, Applied Epic, QQ Catalyst, AgencyZoom, Tarmika |
| **Indio** (Applied) | Digital commercial applications + e-sign | Applied ecosystem | (See Tier 5) |
| **Insurance Website Builder** (ITC/Zywave) | Agency websites + lead capture | Native Zapier | Forms trigger Zaps into EZLynx / Better Agency |

-----

## Tier 9 — Billing & payments

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **Ascend** | Agency billing, payments, premium finance, commission splits | API | Single invoice link; auto-disburses to carriers; HawkSoft partner |
| **Stripe** | General payments | Native Zapier + API | Universal; pairs with invoicing |

-----

## Tier 10 — Communications (phone / SMS / AI intake)

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **RingCentral** | Cloud phone / messaging / video | Native Zapier + API | HawkSoft solution partner |
| **CallRail** | Call tracking + attribution + transcription | Native Zapier + API | Trigger: "phone call completed" w/ full transcript |
| **Smith.ai** | AI + live virtual receptionist / intake | Native Zapier + API | Outbound receptionist call can fire from a form |
| **Twilio** | Programmable SMS / voice | Native Zapier + API | Backbone for custom texting flows |
| **Lightspeed Voice** | Insurance-focused VoIP | Partner API | Common InsuredMine/Better Agency pairing |

-----

## Tier 11 — Websites & e-commerce

| Platform | What it does | Connects via | Notes |
|---|---|---|---|
| **Shopify** | E-commerce storefront + checkout | Native Zapier + GraphQL API | Triggers for new order/customer/product; full store automation |
| **Webflow** | Visual website + CMS builder | Native Zapier + API | CMS collection automation; pairs with Shopify for storefronts |
| **WordPress** | CMS / website platform | Zapier + REST API | Most flexible; huge plugin ecosystem |
| **GoHighLevel** | All-in-one site + CRM + marketing + SMS | Zapier + webhooks + API | Agencies rebill this to clients; strong for funnels/automation |
| **Forge3 / BrightFire** | Insurance-specific agency websites | Forms → Zapier/AMS | Built for compliance + agency lead capture |

-----

## Tier 12 — Farmers Insurance intelligence (portal automation)

Farmers and most carrier portals have **no public API/Zapier app**, so the path is browser-agent automation — the same approach as your existing `home-renewals` and `run-dbb-quotes` skills.

| Target | What it does | Connects via | Notes |
|---|---|---|---|
| **Farmers Agent portal** | Renewal alerts, book of business, policy data | Portal / agent (CoWork skill) | Your `home-renewals` skill already filters homeowners renewals and extracts policy fields |
| **Automated renewal tools** | Pull renewals → extract → quote/remarket → mail/notify | Portal / agent + Zapier downstream | Chain: portal scrape → JSON → DBB quoting skill → AgencyZoom/PostGrid |
| **Alta home quoting** | Farmers home quote generation | Portal / agent (CoWork skill) | Same scripted-portal pattern; not exposed via public API |
| **Browser-agent layer** | Drives no-API portals reliably | Browserbase / Skyvern / Claude Cowork | The general solution to "carrier has no API" (see Tier 14) |

-----

## Tier 13 — Custom LLM & GPU infrastructure (Valya AI)

| Option | What it does | Connects via | Notes |
|---|---|---|---|
| **Anthropic (Claude) API** | Frontier model; agents, extraction, drafting | Native Zapier + API | Best reasoning; OpenAI-compatible patterns via SDK |
| **OpenAI / Google Gemini** | Frontier model APIs | Native Zapier + API | Multi-model fallback options |
| **OpenRouter** | One API → many models (route/fallback) | API | Great for swapping models without re-plumbing |
| **Together AI / Fireworks AI** | Serverless open-model inference (Llama/Qwen 70B+) | API | Per-token (~$0.90/1M tokens for 70B class on Fireworks) |
| **Baseten** | Production model APIs + **dedicated** deployments (Truss) | API | Dedicated GPU control; good for custom checkpoints |
| **Modal / Replicate** | Serverless GPU + model hosting | API | Fast to ship; per-second billing |
| **Groq** | Ultra-low-latency inference | API | When token speed matters |
| **Lambda / CoreWeave / RunPod** | **Dedicated NVIDIA Blackwell (B200)** bare-metal/cloud | API + SSH/K8s | B200 ~$2.65–5.98/GPU/hr; CoreWeave reserved cheapest, RunPod fastest to spin up |
| **Ollama / LM Studio / vLLM** | Run models locally | Local API | On your Digital Storm 2× RTX 5090 (Blackwell) box for 70B work — no per-token cost |

> Practical split for you: Claude API for reasoning/agents, a serverless host (Fireworks/Baseten) for cheap open-model batch jobs, and your local 2× 5090 box (Ollama/vLLM) for private/no-cost inference. Step up to a dedicated B200 (Lambda/CoreWeave) only when local VRAM caps you.

-----

## Tier 14 — Automation orchestration & agentic / AI tooling

| Tool | Category | Connects via | Why it matters to you |
|---|---|---|---|
| **Zapier** | Orchestration (you use) | — | Fastest for app-to-app; Code steps for custom logic |
| **Make** | Visual orchestration | Native + API | Cheaper at high volume; better branching |
| **n8n** | **Self-hostable** orchestration | API / self-host | Run it on your own server → Valya AI owns the stack, no per-task fees |
| **Pipedream** | Code-first orchestration | API | Best when you live in JS/Python |
| **Browserbase / Skyvern** | Headless browser agents | API | Drives carrier portals with no API (Farmers, Alta) |
| **Browse AI / Apify** | Scraping + monitoring | Native Zapier + API | Watch portals/sites; turn pages into structured data |
| **Sensible / Airparser / Docsumo / Reducto / LlamaParse** | Document AI / extraction | API | Pull data from dec pages + ACORD PDFs (complements your pdfplumber work) |
| **Clay** | Data enrichment + AI research | API + Zapier | Enrich leads/commercial prospects at scale |
| **Vapi / Bland AI / Retell AI** | AI voice phone agents | API | Auto-call for renewals, intake, reminders |
| **ElevenLabs** | Voice synthesis | Native Zapier + API | Natural voice for the agents above |
| **PandaDoc / DocuSign** | E-sign + docs | Native Zapier + API | DocuSign already in your connector set |

-----

## Tier 15 — Adjacent industries to productize (same toolkit, new verticals)

Valya AI can re-point this exact stack at neighboring industries. The CRMs/platforms below all have Zapier or APIs.

| Industry | Core platforms | Hook for you |
|---|---|---|
| **Real estate** | Follow Up Boss, BoldTrail (kvCORE), Lofty, Sierra Interactive | You just bought in Sandpoint — you know the workflow |
| **Mortgage / lending** | Encompass (ICE), Blend, Floify, LendingPad | Canopy Connect already plugs into Encompass |
| **Title / escrow** | Qualia, SoftPro | Natural attach to real estate + lending |
| **Property management** | AppFolio, Buildium, DoorLoop | COI tracking + tenant comms overlap |
| **Construction / field services** | Procore, ServiceTitan, Jobber, Housecall Pro | Direct tie to your contractor COI work (KC Striping, Pegasus) |
| **Legal** | Clio, DocuSign, LegalZoom | Already connected to two of these |
| **Accounting / bookkeeping** | QuickBooks, Xero, Bill.com | QuickBooks already in your connectors |

-----

## Appendix A — "Sign in with Google / Microsoft" = OAuth

The term you're reaching for is **OAuth 2.0** (authorization) plus **OpenID Connect / OIDC** (the identity layer on top).

- **Protocol:** OAuth 2.0 + OIDC — the app gets a short-lived **access token** (and an OIDC **ID token**) instead of the user's password.
- **What users see:** "Sign in with Google" / "Sign in with Microsoft" — casually called **social login** or **SSO** (single sign-on).
- **To build it in a Valya AI app:** register an OAuth app with each provider — Google (Google Cloud → OAuth consent screen) and Microsoft (Entra ID → app registration) — then use "Sign in with Google/Microsoft" buttons. Libraries like Auth0, Clerk, or Supabase Auth wire this up in minutes.
- **Relevant to your migration:** because you're moving to Google Workspace (valyaai.us), Google would be your primary identity provider; add Microsoft for clients still on Outlook/365.

-----

## Appendix B — Valya AI brand assets (Google Drive)

**Connected Drive account:** `nate@bingelinsuranceagency.com` (verified May 2026 — this is the account the Google Drive connector authenticates as, *not* the valyaai.us Workspace).

The logo lives in your **Valya AI** folder, with copies in its subfolders:

| File | Use | Size | File ID | View link |
|---|---|---|---|---|
| **vAI.png** | Primary full-res logo | ~1.48 MB | `1SDGVQEynlbzHB7FyrytmBJzcO_A4sNBW` | https://drive.google.com/file/d/1SDGVQEynlbzHB7FyrytmBJzcO_A4sNBW/view |
| **vAI_512.png** | 512px app icon / favicon | ~58 KB | `1jdbt0ko-h5a7xe63y3SZEyik6PtquSOE` | https://drive.google.com/file/d/1jdbt0ko-h5a7xe63y3SZEyik6PtquSOE/view |
| vAI_AZ_dashboard.png | AgencyZoom dashboard screenshot (not a logo) | ~1.5 MB | `1V_W5YSpbFgylLbnT9Hdueq0yNA3-kxXe` | https://drive.google.com/file/d/1V_W5YSpbFgylLbnT9Hdueq0yNA3-kxXe/view |

**How to access it:**

1. **Browser** — open `https://drive.google.com/file/d/<FILE_ID>/view` while signed in as nate@bingelinsuranceagency.com.
2. **Google Drive connector (in Claude)** — search `title contains 'vAI' and mimeType contains 'image/'`, then pull by File ID. Note: connector reads of binary images can be flaky; if it stalls, use the fallback.
3. **Fallback (most reliable)** — download vAI.png from Drive and drag it into the chat, and I can use it immediately in a branded deliverable.

> Web-deploy note: drop `vAI.png` and `vAI_512.png` into this repo's `public/` folder. The site references `/vAI.png` (nav logo) and `/vAI_512.png` (favicon / apple-touch-icon). Until those files exist, the nav falls back to a gradient "V" badge.

-----

## Two cleanest build paths

1. **Zapier-native chain** — Canopy Connect → AgencyZoom → (Thanks.io / RingCentral / Stripe). Everything has a real Zapier app; no middleware.
2. **API + middleware** — For HawkSoft, Applied Epic, AMS360, Momentum AMP, Herald, or any carrier portal: a small Replit/n8n service calls the API (or drives the portal with a browser agent) and hits a Zapier Catch Hook / Code step. Same pattern as the AgencyZoom file-download middleware.
