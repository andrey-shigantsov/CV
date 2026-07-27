---
updated: 2026-07-27T23:50:35+06:00
---

# Andrey Shigantsov
**Senior Rust Backend Developer**

[a.shigantsov@gmail.com](mailto:a.shigantsov@gmail.com) | Telegram: [@rasaro89](https://t.me/rasaro89) <br>
GitHub: [github.com/andrey-shigantsov](https://github.com/andrey-shigantsov) | GitLab: [gitlab.com/andrey-shigantsov](https://gitlab.com/andrey-shigantsov) <br>
Portfolio: [presentation](https://docs.google.com/presentation/d/1cu0rpvXFcqgHSNspt4M0GizctlspQlxM6nvBHP9CE2k/edit?usp=sharing)

---

## SUMMARY

Senior Rust backend developer, 14+ years of experience. I build production backends in Rust: from microservices and Solana smart contracts to embedded software (including C/C++).

I set engineering standards in the team: TDD, code review, technical documentation. I use AI-agent workflows as one of the development tools — planning → agent implementation → multi-stage review → manual control — and personally own the quality of the final code. I help streamline business processes: experience as a Scrum Master and running a project as a PM. Ready to grow into a Tech/Team Lead role.

**Desired role**: **Senior Rust Backend Developer** with further growth into Tech/Team Lead, full-time, remote

---

## EXPERIENCE

### **BridgeApp**
**Rust Backend Developer** — Aug 2025 – Jul 2026 (11 months) <br>
*Remote · Distributed team of Rust developers · Agile*

Collaboration platform. Backend development in Rust (tokio, gRPC, Kafka/Redpanda, Redis, sqlx + PostgreSQL).

- Designed and rolled out an integration auto-testing system for gRPC services (sqlx-based tests in Rust) — by own initiative, where no automated testing had existed before; it became the company-wide testing standard.
- Implemented health-checks across the entire backend (20+ microservices), each probing its own state and its dependencies on other services and external systems (Kafka, PostgreSQL, Redis).
- Extended the `tasks` and `history` microservices to power the front-end home page.
- Added a templated marketing-email system to the CRM microservices.
- Unified data filtering by arbitrary fields (including user-created custom fields) across the `databases` and `tasks` services.
- **Open source:** [github.com/MathAndMagic/bql](https://github.com/MathAndMagic/bql) — authored the spec for the BQL unified query language and a generator that produces parser + formatter libraries for all required languages (Rust, TypeScript, Swift, Kotlin).
- Contributed to the refinement, refactoring, and bug-fixing of critical microservices (`idm`, `messenger`, `projects`, `tasks`).

### **STREAM TECH LLC (ООО «СТРИМ ТЕХ»)**
**Rust Backend & Solana Developer** — Nov 2022 – Aug 2025 (2 years 9 months) <br>
*Remote · Distributed team of Rust developers · Agile*

Backend services and on-chain programs for blockchain products.

- Developed Rust backends (tokio, PostgreSQL, Solana).
- Developed and maintained smart contracts for the Solana blockchain.
- **Open source:**

  - [github.com/texture-fi/price-proxy](https://github.com/texture-fi/price-proxy) — Solana contract providing unified access to fresh prices from multiple arbiters; developed the system core and the testing system.
  - [github.com/texture-fi/common/tree/master/macros](https://github.com/texture-fi/common/tree/master/macros) — shared macros used across all contracts, programs, and services.
  - [github.com/texture-fi/anchor-interface](https://github.com/texture-fi/anchor-interface) — lightweight library for interacting with `anchor-lang` smart contracts.

### **TRADETECH DEVELOPMENT LLC (ООО «Трейдтех Девелопмент»)**
**Rust Backend & Solana Developer** — Apr 2021 – Nov 2022 (1 year 8 months) <br>
*Fully remote · Distributed team of Rust developers · Agile*

High-load microservices and Solana DeFi infrastructure. Held partial project-lead responsibilities alongside development.

- **Project-lead duties:** team coordination, task tracking in Jira, planning and organizing work, daily progress monitoring, reporting on results.
- Built high-load microservices on async-I/O Rust (tokio, serde, prost, ClickHouse).
- Developed smart contracts for the Solana blockchain.
- **Key achievement — DEX-connector smart contract** (Leveraged Staking project for texture.finance): a Solana contract for unified token exchange across multiple decentralized exchanges. At the time of writing it supported Orca / Whirlpools; the contract executes large-volume swaps distributed over time in small portions to minimize market impact.
- **Key stack applied on the project:**

  - **Solana:** shipped smart contracts with automated test suites (`solana-program-test`, `solana-test-validator`) and Rust-client integration.
  - **ClickHouse:** owned schema design and maintenance, ran migrations via `golang-migrate`, integrated via the Rust client.
  - **Grafana + Prometheus:** instrumented Rust services with metrics and built advanced observability dashboards.
  - **Apache Kafka:** implemented high-throughput consumers in Rust.
  - **Docker:** containerized services for deployment.

### **KV-SVYAZ (НПООО «КВ-связь»)**
**C/C++ Programmer** — Mar 2017 – Sep 2019 (2 years 7 months) <br>
*Software Development Project Lead / Scrum Master* — Mar 2019 – Aug 2019 (6 months)

Embedded and application software for communication systems.

- Developed embedded software in C (HOST, DSP) on Cortex-Mx and TMS320C674x cores.
- Developed application software in C++ with Qt.
- Authored technical documentation and typeset documents in LaTeX.
- **As Project Lead / Scrum Master:** strategic and operational planning, delivery to the customer, and oversight of the development process.

### **Freelance**
**Software Engineer (C/C++)** — Apr 2015 – Apr 2016 (1 year 1 month)

Contract embedded and application software for communication systems and devices.

- Developed embedded software in C (HOST, DSP) on Cortex-Mx and TMS320C55xx cores and application software in C++ with Qt; authored and typeset technical documentation in LaTeX.
- **NAVDAT-RUS receiver prototype** for Central Research Institute "Kurs" (ЦНИИ «Курс»): a specialized OFDM communication channel — built the Intel-PC-based transmitter and the ZedBoard/Linux-based receiver, plus a PC-based channel test.
- **PC-1000 POS terminal firmware:** built the firmware, the `cmake` toolchain, and a PC simulator for debugging.

### **Omsk Scientific Research Institute of Instrument Engineering OJSC**
**Software Engineer (2nd category)** — Feb 2010 – Mar 2015 (5 years 2 months)

Embedded and application software for communication and navigation systems.

- Developed embedded software in C (HOST, DSP) on Cortex-Mx and TMS320C55xx cores and application software in C++ with Qt; authored technical documentation.
- Self-taught microcontroller programming and the fundamentals of digital signal processing (DSP) on the job — the foundation for all later embedded work.
- **NAVTEX "Fregat" receiver** ([product](http://www.oniip.ru/produkcia/detail.php?SECTION_ID=120&ELEMENT_ID=745)): participated in development and certification; built the NAVTEX transceiver, its test suite (incl. on PC), and parts of the GUI, INS, and Alarm services.

---

## EDUCATION

**Specialist Degree, Information Security (Comprehensive Information Security of Automated Systems)** <br>
Siberian State Automobile and Highway Academy (СибАДИ) <br>
2006 – 2011

---

## SKILLS

- **Methodologies:** Agile/Scrum
- **Languages:** Rust (primary), C/C++
- **Backend:** tokio, gRPC, REST, serde, prost, async-I/O
- **Data & Messaging:** PostgreSQL (sqlx), ClickHouse, Redis, Apache Kafka / Redpanda
- **Blockchain / Solana:** smart contracts, `anchor-lang`, DEX integrations, `solana-program-test`, `solana-test-validator`
- **Observability:** Prometheus, Grafana
- **Tooling & DevOps:** Docker, Git, CI/CD
- **Documentation:** Markdown, LaTeX
- **AI-Assisted Development:** AI-agent workflows (planning → implementation → review loop), agent rules & skills engineering, tech docs as persistent agent memory
- **Spoken languages:** Russian (Native), English (A2 – Pre-Intermediate)

---

## RECOMENDATIONS

![recomendation-v-latish_eng](./Recomendations/20260717_a-shigantsov_recomendation-v-latish_eng.jpg)
