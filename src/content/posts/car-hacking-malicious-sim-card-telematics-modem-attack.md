---
title: "Car Hacking Just Got a New Front Door: The SIM Card Inside Your Telematics Modem"
slug: "car-hacking-malicious-sim-card-telematics-modem-attack"
pubDate: 2026-08-13T11:13:30.000Z
updatedDate: 2026-08-13T11:13:30.000Z
author: "Luciano Ferrari"
description: "Birmingham and Fuzzware researchers showed that a malicious SIM can execute code on the cellular modems inside cars, EV chargers, and industrial IoT. For automotive engineers, that's a new perimeter — below the stack you already test."
tags: ["car hacking", "automotive security", "iot security", "Cellular Security", "Telematics", "SIM Toolkit"]
tagSlugs: ["car-hacking", "automotive-security", "iot-security", "cellular-security", "telematics", "sim-toolkit"]
featured: false
image: "/content/images/2026/08/car-hacking-20260813-110639.webp"
imageAlt: "car hacking — featured image"
metaTitle: "Car Hacking via Malicious SIM: Modem Attack Chain"
---

Your car's cellular modem trusts the SIM card sitting inside it. That trust is not audited, not sandboxed, and — as of last week — remotely exploitable. For anyone doing **car hacking** work in 2026, this is the finding that quietly rewrites the threat model: the SIM is now a command channel into the modem, and the modem sits below the layer your current pentest tools reach.

Researchers at the University of Birmingham and the security firm Fuzzware tested 26 phones and cellular modules and found that a malicious SIM can issue SIM Toolkit (STK) commands the modem executes without meaningful verification ([reported by The Hacker News](https://thehackernews.com/2026/08/a-malicious-sim-card-can-run-attacker.html)). On a phone, the OS sandbox absorbs most of the blast radius. On the cellular module bolted into an EV charger, an industrial router, or a car's telematics control unit (TCU), there is no such sandbox. The modem *is* the perimeter. And the modem now runs attacker code.

This post walks through what changed, why it matters more for cars than for phones, the realistic attack chain from rogue SIM to CAN bus, and what hands-on car hacking work actually reveals that a spec review never will.

## The SIM Card You Trust Is Also a Command Channel

SIM Toolkit is a set of proactive commands defined in [ETSI TS 102 223](https://www.etsi.org/deliver/etsi_ts/102200_102299/102223/). The design assumption from three decades ago was straightforward: the carrier owns the SIM, the SIM is trusted, and the SIM can ask the handset to do useful things — display a menu, send an SMS, open a data channel, launch a browser, run a location request. The modem is expected to comply.

Fast-forward to a modern cellular IoT deployment and that assumption ages badly. A Quectel, u-blox, or Telit module inside a telematics unit is not a handset with a user tapping "Allow." It's a headless component wired to the vehicle's internal buses, with the modem firmware executing SIM-originated commands as a matter of routine. The Birmingham/Fuzzware work showed that on many of these modules, commands issued by a rogue SIM traverse the modem's parser into memory regions that were never hardened against a hostile card. Where the paper gets uncomfortable is the specifics: parser bugs, missing length checks, and command handlers that assume well-formed input because "the SIM would never send malformed data."

The SIM would. The SIM does. And once the modem executes an unchecked command, whatever privilege the modem firmware holds is now attacker-controlled.

## Why Automotive Modems Are More Vulnerable Than Smartphones

Here is the piece that should keep automotive OEMs up at night: phones got lucky because they were built on top of a general-purpose OS with its own memory protection, privilege separation, and — crucially — a modem-to-application-processor boundary policed by an IPC layer. When a modem misbehaves on a phone, it takes work to escalate into Android or iOS.

Telematics units are a different animal. A typical automotive cellular module is a system-on-module with the baseband, a Cortex-A application core, and direct access to peripheral buses — often including UART or SPI links that terminate on gateway ECUs bridging to the vehicle CAN or CAN-FD bus. Some designs run the modem firmware as the *only* firmware. There is no application processor above it to contain a compromise. The modem talks directly to the vehicle.

Add three uncomfortable facts:

- Automotive cellular modules stay in the field for 10–15 years without meaningful firmware updates. The module in a 2019 vehicle is running 2018-vintage baseband code today.
- SIMs in automotive deployments are frequently soldered eUICC / iSIM parts provisioned over-the-air. The provisioning profile — the thing that becomes the "SIM" logically — can be pushed remotely by the carrier. Compromise the carrier profile server, and you compromise every vehicle that pulls a profile from it.
- The pentesting team hired to test the vehicle almost always tests the infotainment head unit, the mobile app, and the cloud backend. The modem inside the TCU is a black box on the hardware BOM — not on the pentest scope.

The modem is the new perimeter. Nobody is testing the perimeter. That is the shape of the problem, and it is why traditional car hacking curricula that stop at CAN injection are already a generation behind.

## Attack Chain: From Rogue SIM to CAN Bus Control

The realistic attack chain has three plausible entry points and one payoff. Let's walk it:

### Entry: how the attacker's SIM gets in front of the modem

- **Supply-chain interdiction.** A batch of eSIM profiles or physical SIMs is tampered with somewhere between the SIM vendor and the OEM's production line. This is the same class of attack academic supply-chain researchers have documented for other components; SIMs are no different, and the auditing is weaker.
- **Malicious or compromised MVNO.** The vehicle's cellular connectivity is often provisioned through a mobility-focused MVNO. If that carrier's profile server is compromised — or if the MVNO itself is hostile — the profile pushed to the eUICC contains attacker-controlled applets.
- **Rogue base station + SIM re-provisioning flows.** With an [SDR-based base station](https://www.ettus.com/all-products/usrp-b210/) emulator, an attacker within RF range can coerce the modem into re-registering, then abuse OTA SIM update mechanisms (SMS-based OTA, BIP channels) to push a modified applet into an existing card.

### Exploit: STK command triggers modem code execution

Once the malicious applet is resident, it issues a SIM Toolkit proactive command that hits a vulnerable handler in the modem firmware. The Birmingham/Fuzzware work found this in real, shipping modules — not theoretical ones. Common bug classes: unchecked TLV length fields, integer overflows in the command dispatch table, and format-string-adjacent flaws in the DISPLAY TEXT and SET UP CALL handlers.

### Payoff: what the compromised modem can now do

- Read and inject frames on any bus the TCU touches — including, in poorly-segmented architectures, the vehicle CAN bus. Unlock, start, disable ADAS, spoof sensor readings.
- Hijack telemetry uploads: false crash reports, false location, silent stalking of the vehicle owner.
- Pivot to the head unit over the internal Ethernet or CAN bridge in vehicles that don't enforce strict domain isolation.
- Persist across ignition cycles by writing to the modem's own flash — invisible to any host-side scanning the OEM might do.

None of these steps require the attacker to touch the vehicle physically after the initial provisioning. That is what makes this class of finding different from prior [automotive security research on the LufSec blog](/) that assumed OBD-II access or an infotainment exploit as the beachhead.

## What OEMs Miss (And What Hands-On Testing Reveals)

Here is the objection I hear from experienced pentesters when I describe this attack surface: *"I already do penetration testing on the application layer, the mobile app, and the cloud backend. Why do I need to learn modem-level attacks?"*

Because the modem is now the perimeter, and your current toolchain doesn't reach it. Burp will not find this. A cloud pentest will not find this. Even a well-scoped hardware pentest that terminates at "we dumped the TCU firmware and looked for hardcoded creds" will not find this — because the vulnerability isn't in the firmware image the TCU boots. It's in how that firmware handles a class of input the tester never generates: proactive commands from a hostile SIM, delivered over a channel the tester doesn't emulate.

The gap between "reading the ETSI spec" and "finding the bug" is the same gap between reading the CAN spec and successfully injecting arbitrary UDS diagnostic sessions on a live vehicle. Both are learnable. Neither is learned from documents. Real car hacking capability comes off the bench, not off the page.

What hands-on testing actually looks like for this class of bug:

- A live telematics module on the bench, powered, with its RF frontend routed into a Faraday enclosure.
- A software-defined radio running an open-source cellular stack (srsRAN, OpenAirInterface, or Osmocom's cellular tooling) configured as a rogue base station the modem will attach to.
- A programmable SIM (sysmoISIM-SJA2 or similar) hosting a Java Card applet the tester wrote to emit malformed proactive commands.
- A fuzzer instrumenting the STK command dispatcher — either coverage-guided against an emulated modem, or blackbox against the live module with a debug UART for observation.
- A CAN interface on the vehicle-side of the TCU, so when the modem does something interesting, you can see what leaks onto the bus.

This is not exotic. It is standard bench for anyone doing serious cellular IoT security work in 2026. What is exotic is finding a course that teaches it against real automotive hardware instead of a lab full of generic dev boards. Most "IoT security" curricula stop at the Wi-Fi and BLE layer because the RF equipment gets expensive and the vendor NDAs get complicated. That's why the same finding keeps getting rediscovered by a small circle of academic labs — not because it's hard, but because almost nobody is set up to look.

If your background is web or infrastructure pentesting and you're wondering where the on-ramp is: our [hands-on IoT hacking course](https://lufsec.com/courses/iot-hacking) covers the firmware extraction, UART/JTAG bringup, and RF fundamentals you'll want before touching a telematics module. If you're an embedded engineer looking at the broader offensive-security ladder, the full [Lufsec course catalog](https://lufsec.com/courses/) maps the progression from firmware analysis into vehicle-specific work.

## The Practical Takeaway for Car Hacking Teams

Three things automotive security teams should do this quarter:

1. **Ask your Tier 1 which cellular module is in your TCU, and whether they have a documented response to the Birmingham/Fuzzware STK findings.** If the answer is a blank stare, that is your first bug report.
2. **Inventory your SIM provisioning path.** Who controls the eUICC profile server? What audits exist? What is the applet update process, and who signs it?
3. **Get a live module on a bench and try the attack yourself.** The gap between reading this post and reproducing the finding on your own hardware is where real capability lives. If your team can't do that today, that's the skill investment.

## Learn to Break the Modem Before Someone Else Does It in Your Fleet

If you're hardening a connected vehicle in 2026, you need to fuzz the same modems the researchers did — with the same rogue-base-station and hostile-SIM tooling, against live telematics hardware, on your own bench. Reading about the attack is not the same as reproducing it, and reproducing it is not the same as being able to find the next one.

[**Lufsec's Car Hacking Course**](https://lufsec.com/courses/car-hacking?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=car-hacking&utm_content=primary) is built for the embedded and automotive security engineer who wants to add offensive skills against real vehicle hardware. You will work with live telematics modules, SDR-based cellular tooling, programmable SIMs, and CAN/CAN-FD interfaces on the same class of gear the Birmingham and Fuzzware researchers used. You'll leave with a bench you can rebuild at work, a methodology for fuzzing modem firmware, and the reflexes to spot the next STK-class bug before it hits your fleet. It is, as far as we know, the only car hacking course that puts all of that hardware in your hands instead of talking around it.

*Not ready for the Car Hacking Course yet? Start with our free* [*Cybersecurity Career Guide*](https://www.lufsec.com/products/digital_downloads/cyber-security-career-guide?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=car-hacking&utm_content=secondary) *— a short read that maps the offensive-security ladder from web and infrastructure work into embedded, RF, and vehicle security, so you can plan the next step honestly before committing to the hardware track.*
