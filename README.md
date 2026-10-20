<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="Assets/zenoska-banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="Assets/zenoska-banner-light.svg">
    <img src="Assets/zenoska-banner-dark.svg" alt="OSKA Ecosystem Banner" width="100%">
  </picture>
</p>

<h1 align="center"><b>OSKA Organization Defaults &amp; Core Assets</b></h1>
<p align="center">
  <code>ZenOska/.github</code> • Canonical repository health files, brand assets, and organization landing profile.
</p>

<p align="center">
  <a href="https://zenoska.github.io/wiki/">
    <img src="https://img.shields.io/badge/Central_Wiki-D2B063?style=for-the-badge&logo=gitbook&logoColor=white&labelColor=090A0F" alt="Central Wiki">
  </a>
  &nbsp;&nbsp;
  <a href="profile/README.md">
    <img src="https://img.shields.io/badge/Landing_Profile-README.md-D2B063?style=for-the-badge&logo=markdown&logoColor=white&labelColor=090A0F" alt="Landing Profile">
  </a>
  &nbsp;&nbsp;
  <a href="https://github.com/ZenOska">
    <img src="https://img.shields.io/badge/License-Apache_2.0-D2B063?style=for-the-badge&labelColor=090A0F" alt="Apache 2.0 License">
  </a>
</p>

<hr>

## Overview

This repository houses the organization-wide defaults, canonical brand assets, and configuration standards for **OSKA** (hosted on GitHub under the organization handle [`ZenOska`](https://github.com/ZenOska)).

Everything configured here sets the default presentation and baseline standards across every repository in the organization.

---

## Repository Structure

```
.github/
├── Assets/
│   ├── mascot/
│   │   └── mascot.png              # High-resolution brand mascot
│   ├── v1/                         # Early vector draft iterations
│   ├── vfinal/                     # Production vector master exports
│   ├── zenoska-banner-dark.svg     # Adaptive dark mode banner
│   ├── zenoska-banner-light.svg    # Adaptive light mode banner
│   ├── zenoska-logo-dark.svg       # Dark theme logomark
│   └── zenoska-logo-light.svg      # Light theme logomark
├── profile/
│   ├── Assets/                     # Mirrored asset pack for profile rendering
│   └── README.md                   # Public landing profile for github.com/ZenOska
└── README.md                       # This repository reference guide
```

---

## Core Components

### 1. Organization Landing Profile (`profile/README.md`)
GitHub automatically renders [`profile/README.md`](profile/README.md) on the main landing page of [`github.com/ZenOska`](https://github.com/ZenOska). It introduces OSKA's mission, defines our core philosophy around **Sovereign Machine Cognition**, and displays our four architectural principles:
- **`01` — Intelligence is engineered**: Investigating cognition through working software and tangible architectures.
- **`02` — Autonomy begins with control**: Transparent execution environments running locally without hidden dependencies.
- **`03` — Complexity should compose**: Independent, modular subsystems combining cleanly into cohesive systems.
- **`04` — Ideas must become artifacts**: Empirical implementation to validate theoretical concepts.

### 2. Brand Identity Assets (`Assets/`)
The `Assets/` directory stores production-ready vector SVG files and artwork for use across documentation, repositories, and release distributions:
- **Adaptive SVG Banners**: Media-query switching for GitHub web interfaces and IDE previewers.
- **Vector Logomarks**: Scalable brand insignias in dark and light obsidian-gold variants.
- **Brand Mascot**: Located in `Assets/mascot/mascot.png`.

---

## Asset Usage Guidelines

When referencing organizational assets in child repositories or documentation, use absolute GitHub raw links or relative organization paths:

```markdown
<!-- Adaptive Banner -->
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/ZenOska/.github/main/Assets/zenoska-banner-dark.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/ZenOska/.github/main/Assets/zenoska-banner-light.svg">
  <img src="https://raw.githubusercontent.com/ZenOska/.github/main/Assets/zenoska-banner-dark.svg" alt="OSKA Banner" width="100%">
</picture>
```

---

## Ecosystem Navigation

- **Organization Hub**: [github.com/ZenOska](https://github.com/ZenOska)
- **Central Documentation**: [zenoska.github.io/wiki](https://zenoska.github.io/wiki/)
- **Landing Profile**: [`profile/README.md`](profile/README.md)
- **Issue Tracking**: [ZenOska/.github Issues](https://github.com/ZenOska/.github/issues)

---

<p align="center" dir="auto">
  <sub><i><b>Maintained by the OSKA Core Team • Sovereign Computing Environments</b></i></sub>
  <br>
  <sub>Independent by intent. Experimental by nature.</sub>
</p>