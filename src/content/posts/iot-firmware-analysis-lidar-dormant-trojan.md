---
title: "IoT Firmware Analysis After the LiDAR Trojan: Why Dormant Payloads Break Surface Testing"
slug: "iot-firmware-analysis-lidar-dormant-trojan"
pubDate: 2026-06-17T12:42:54.000Z
updatedDate: 2026-06-17T12:42:54.000Z
author: "Luciano Ferrari"
description: "A new arXiv paper shows malware can sit dormant in LiDAR firmware and wake up to a modulated light pulse — no network, no hardware access. Here's what that means for IoT firmware analysis."
tags: ["iot security", "firmware analysis", "reverse engineering", "Embedded Security", "Threat Research"]
tagSlugs: ["iot-security", "firmware-analysis", "reverse-engineering", "embedded-security", "threat-research"]
featured: false
image: "/content/images/2026/06/iot-firmware-analysis-20260617-lidar-regen---9012a289-3530-4992-91f9-e7ac4df078de-1.webp"
imageAlt: "Disassembled LiDAR sensor on a lab bench — featured image"
metaTitle: "IoT Firmware Analysis: LiDAR Dormant Trojan Lesson"
---

A paper landed on arXiv this week that should change how you scope an IoT firmware analysis engagement. The researchers describe a Trojan that lives inside a LiDAR sensor's firmware, stays completely quiet through every normal operating condition, and activates when it sees a specifically modulated optical signal aimed at the sensor. No network traffic. No exposed port. No physical access at trigger time. The payload waits in the firmware, and the world walks past it.

The paper is [*Anywhere, Any-Stymie: Remote Activation of Trojan Malware on LiDAR with Modulated Signals*](https://arxiv.org/abs/2606.17562v1), published 16 June 2026. The mechanics are interesting on their own, but the practitioner implication is bigger: this attack succeeds because every standard testing layer was blind to it. Network monitoring saw nothing. Behavioral fuzzing saw nothing. Even a careful firmware audit, if it didn't ask the right questions, would have shipped this thing into production.

If you do IoT firmware analysis for a living — or you're trying to move past surface-level IoT pen testing into the kind of work that actually catches sophisticated implants — the LiDAR case is a useful forcing function. Let's pull it apart.

## The attack that waits: how an optical trigger bypasses every layer of network defense

The core mechanic is straightforward once you say it plainly. A malicious actor — supply-chain insider, compromised contract manufacturer, or a clever hardware reseller — modifies the LiDAR firmware to include two things: a dormant payload, and a trigger-recognition routine that watches the sensor's own input stream for a pattern that doesn't occur naturally. In this case, the trigger is a modulated light signal that maps onto the LiDAR's photodetector pipeline. When the sensor sees the right pattern, the trigger routine fires and the payload activates.

Read that again. The trigger arrives through the *sensor's primary function*. It's not a backdoor port. It's not a command-and-control beacon. It's the device doing exactly what it was built to do — measure light — and one of those measurements happens to be a wake-up call.

This is why every network-centric defense fails. There is no malicious packet. There is no anomalous outbound connection until the payload activates, and by then the trigger has already won. The attacker stood in a parking lot with a modulated laser and lit up a sensor on a passing vehicle. That's the threat model.

The same pattern generalises. Replace LiDAR with a microphone (modulated ultrasonic — see the well-documented [SurfingAttack research](https://surfingattack.github.io/) for an existence proof on commodity voice assistants), a camera (steganographic light or QR-like patterns in the visual field), a temperature sensor (precisely timed heating cycles), or a radio receiver (an in-band signal that's syntactically valid but semantically a trigger). Any sensor that interprets a signal can, in principle, be wired to interpret a specific signal as *start running the dormant code*.

## Why standard IoT firmware analysis misses dormant payloads

Most IoT firmware analysis work — including a lot of what gets sold as a "firmware security assessment" — focuses on three things: extracting the filesystem, scanning for known vulnerable binaries and hardcoded credentials, and emulating the firmware to run dynamic tests. All three are useful. None of them catch what the LiDAR researchers describe.

Static binary scanning looks for known-bad signatures. A dormant Trojan written specifically for this device has no signature. It looks like a sensor processing routine because, structurally, it *is* a sensor processing routine — one with an extra branch.

Emulation and behavioural fuzzing run the firmware against synthetic or replayed inputs. If those inputs never include the specific trigger pattern, the payload never activates. The firmware appears to behave correctly. The report says "no malicious behaviour observed." Ship it.

This is the same blind spot we mapped out in our earlier write-up on [firmware kernel lock-in and why surface scans don't see it](/iot-firmware-analysis-kernel-lock-in/): when an attacker controls the firmware's structure, surface analysis grades the attacker's homework. To find this kind of implant you have to move from "does the firmware behave?" to "what is the firmware *capable of*, given any reachable input?" That shift is what serious IoT firmware analysis actually demands.

That's a different question, and it needs different techniques.

## Three IoT firmware analysis techniques that would have caught the trigger logic

None of these are exotic. They're standard in serious reverse-engineering work and rare in commodity IoT assessments. That gap is the opportunity.

**1. Reachability analysis on input-handling code paths.** Start from every routine that touches sensor input — ADC handlers, DMA callbacks, decoder routines — and walk forward. Any branch that conditions execution on a specific input pattern, especially one that activates code paths unused elsewhere in normal operation, is suspect. The LiDAR Trojan's trigger routine is a branch like this. It's quiet under normal input distributions and loud under a precise one. A reachability map makes that asymmetry visible even when the payload itself is obfuscated.

**2. Symbolic execution of decoder pipelines.** Standard fuzzing throws random or grammar-aware inputs at the firmware. Symbolic execution asks the inverse question: what input would reach *this* branch? Pointing a symbolic executor like [angr](https://angr.io/) at the sensor input pipeline and asking "is there any reachable state that activates this code region?" finds trigger logic even when the trigger itself is bizarre and unlikely. The cost is engineering time and tractable state explosion. The payoff is finding payloads that pure fuzzing would never wake up. We walked through a worked example of this approach on real router firmware in our [Cisco SD-WAN CVE teardown](/cisco-sd-wan-cve-20245-iot-firmware-analysis/).

**3. Live-device differential analysis.** Boot the real device. Instrument it — JTAG, SWD, glitching rig, side-channel probes — and feed it both clean and adversarial input streams. Watch power, timing, memory access patterns, and instruction-trace coverage. A dormant payload changes the device's execution profile the moment it activates. You can see the change in microseconds of timing jitter on a power rail before you see it in any network capture. This is the technique that catches the implants nobody else finds, and it's the one you can't run from a VM.

The first two are firmware-only. The third needs the physical device on a bench. Together, they cover the surface that dormant-Trojan attackers are now provably exploiting.

## From LiDAR to smart locks: mapping external activation surfaces across IoT device classes

Once you accept that any sensor can be a trigger channel, your threat model has to grow an entirely new surface: the *external activation surface*. It's not the network attack surface. It's not the physical attack surface. It's the set of environmental signals the device interprets, and which of those signals could, in principle, encode a wake-up pattern.

Some quick mappings to start the conversation:

- **Smart locks:** capacitive sensors, NFC readers, accelerometers. A specific tap pattern or NFC payload could be a trigger. Most lock firmware assessments don't test for that.
- **Industrial controllers:** Modbus and serial inputs. A syntactically valid but unusual register-write sequence as trigger.
- **Consumer cameras:** visual field. A pattern shown on a screen or printed sticker in the camera's view.
- **Smart speakers:** microphones. Sub-audible or ultrasonic patterns, well documented in academic work, are an obvious trigger channel.
- **Wearables:** Bluetooth advertising packets, accelerometer patterns. A specific motion sequence or beacon pattern.

For each class, the IoT firmware analysis question stops being "does this device have known CVEs?" and becomes "for every input modality this device interprets, what would it take to encode a trigger, and is the firmware actually checking for one?" That's a question you answer with reverse engineering on real hardware, not with a scanner. Our broader [post-mortem on the c0xmo IoT botnet](/iot-security-vulnerabilities-c0xmo-botnet-lessons/) walks through what happens at scale when this kind of question goes unasked across an entire device class.

If you're new to this work and want a low-friction way in, the [free intro to IoT hacking](https://lufsec.com/free/intro-iot-hacking) covers the foundational firmware extraction and analysis workflow you'd build on top of. The LiDAR paper is a forcing function, not a foundation — you still need the foundation.

## What this means for ongoing runtime monitoring

One last point, because it's where a lot of teams will land wrong. If dormant Trojans can hide in firmware, the temptation is to lean harder on runtime monitoring: "we'll catch it when it fires." That's necessary, but it's not sufficient, and on its own it's a losing position.

Runtime monitoring catches the payload *after* it activates. For a LiDAR feeding a safety-critical perception stack, the gap between activation and consequence is measured in milliseconds. By the time your SIEM correlates the anomaly, the vehicle has already swerved, the lock has already opened, the controller has already written the wrong setpoint. Runtime monitoring is a damage-limitation control, not a prevention control.

Prevention lives in IoT firmware analysis. Specifically, in firmware analysis that asks reachability questions, runs symbolic execution against input pipelines, and validates findings on live devices. That's the work the LiDAR paper proves the industry isn't doing at scale yet — and it's exactly the gap that justifies investing in real reverse-engineering capability instead of another scanner subscription. If your assessment program doesn't include any of the three techniques above, the next dormant Trojan is going to ship through it the same way this one would have.

## If you want to do this work for real

This is the kind of practitioner gap the [**IoT Hacking Deep Dive**](https://lufsec.com/courses/iot-hacking?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=iot-deep&utm_content=primary) course was built for. It's for security engineers who already understand the surface — Nmap on a router, Burp on a captive portal — and are ready to work on real devices: firmware extraction over UART and SPI flash, reverse engineering with Ghidra against MIPS and ARM binaries, hardware glitching, and the kind of reachability and decoder-pipeline analysis we just walked through, applied hands-on to consumer and industrial devices on the bench.

You leave knowing how to find the trigger logic before it ships, not after it fires. That's the only side of this attack you want to be on.

[**Enrol in the IoT Hacking Deep Dive →**](https://lufsec.com/courses/iot-hacking?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=iot-deep&utm_content=primary)
