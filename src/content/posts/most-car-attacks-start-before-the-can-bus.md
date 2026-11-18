---
title: "Most Car Attacks Start Before the CAN Bus"
slug: "most-car-attacks-start-before-the-can-bus"
pubDate: 2026-05-11T13:33:22.000Z
updatedDate: 2026-05-11T13:33:22.000Z
author: "Luciano Ferrari"
description: "Most car attacks now start in apps, APIs, telematics, and cloud systems before the CAN bus ever matters. Here are four remote attack paths security teams still under-test."
tags: ["car-hacking"]
tagSlugs: ["car-hacking-2"]
featured: false
image: "/content/images/2026/05/2026-05-11-car-hacking-ghost-hero.jpg"
imageAlt: "Most Car Attacks Start Before the CAN Bus — Car Hacking"
metaTitle: "Most Car Attacks Start Before the CAN Bus | Lufsec"
---

Car hacking is still too often explained like the real battle starts when an attacker reaches the bus.

That is no longer the full story.

Upstream’s 2026 automotive cybersecurity report says 67% of publicly reported incidents in 2025 stemmed from telematics and cloud systems, while S&P Global’s March 2026 software-defined-vehicle analysis warns that always-on connectivity, OTA workflows, and unified software stacks are expanding the attack surface far beyond the in-vehicle network. Kaspersky’s 2026 automotive threat forecast pushes the same lesson from another direction: attackers are increasingly hitting automaker, fleet, and supplier infrastructure because that upstream access can create real downstream impact.

That matters right now because LufSec’s operating data is blunt: paid orders in the last 30 days are still zero, weekly email open rate is still below goal, and the content has been generating attention without generating enough conversion. So tomorrow’s car-hacking piece should not be another vague awareness post. It should give readers a stronger mental model, a practical checklist, and a direct reason to move from free content into paid training.

## The wrong mental model

A lot of teams still talk about automotive security like this:

1. Protect the CAN bus.
2. Lock down diagnostics.
3. Add a gateway.
4. Call it good.

Those layers still matter, but they are no longer the first place many attacks begin.

If an attacker can compromise a mobile app session, abuse weak ownership logic, exploit a backend API, hijack a telematics workflow, or reach a trusted supplier process, the vehicle gateway is not your first broken boundary. It is just the next one.

## Four remote attack paths security teams still under-test

### 1. Companion app authentication and recovery flows

If login, device binding, password reset, MFA fallback, or session refresh is weak, the attacker may not need a vehicle exploit at all. They only need to become the platform’s accepted user.

### 2. Backend APIs and ownership logic

Remote lock, unlock, locate, charging, climate, and vehicle-status actions often depend on backend trust decisions. Weak authorization, poor object-level access control, and sloppy vehicle-account binding can turn a web bug into a car-security bug.

### 3. Telematics and OTA command paths

S&P Global’s SDV analysis highlights how always-on connectivity and continuous updates raise both value and exposure. If telematics services, command brokers, or update flows trust too much, attackers can pivot from cloud-side access toward real vehicle behavior.

### 4. Supplier, fleet, dealer, and support workflows

Kaspersky’s 2026 forecast makes this uncomfortable point clear: attackers increasingly target manufacturer and supplier infrastructure because that is where scale lives. A compromised third-party workflow, support action, or fleet-management process can produce vehicle impact without a dramatic CAN exploit chain.

## What operators should test first

If you want a practical priority list, start here this week:

- Map every path that can issue or approve a remote vehicle action.
- Test account binding and ownership transfer flows like an attacker, not like a normal user.
- Review API authorization separately from basic authentication.
- Trace which supplier or dealer workflows can change trust state, update state, or command state.
- Verify how a remote foothold could cross into the vehicle gateway or other privileged control paths.

That is the operator view most teams still miss.

Car hacking today is not just about what happens on the bus. It is about who the platform trusts before the bus ever comes into play.

If you want hands-on training that matches the way the real attack surface looks now, start with [Car Hacking 101: From Key Fob Cracking to Full System Exploitation](https://www.lufsec.com/products/courses/car-hacking). For supporting context, review Upstream’s [2026 Automotive Cybersecurity Report](https://upstream.auto/reports/global-automotive-cybersecurity-report/), S&P Global’s analysis of [automotive cybersecurity for software-defined vehicles](https://www.spglobal.com/automotive-insights/en/blogs/2026/03/automotive-cybersecurity-for-software-defined-vehicles), and Kaspersky ICS CERT’s forecast on [risks to automotive infrastructure in 2026](https://ics-cert.kaspersky.com/publications/blog/2026/02/19/risks-for-the-automotive-industry-in-2026/). If you want more operator-grade breakdowns across AI hacking, car hacking, and IoT hacking, join the newsletter at [LufSec](/#/portal/signup) and subscribe on [YouTube](https://www.youtube.com/@Lufsec).
