---
title: "Car Hacking Starts in the IT Office: What a French Automotive Breach Reveals"
slug: "car-hacking-starts-in-it-office-french-automotive-breach-tailscale-openssh"
pubDate: 2026-06-18T14:18:56.000Z
updatedDate: 2026-06-18T14:18:56.000Z
author: "Luciano Ferrari"
description: "A French attacker hit an automotive supplier and built a Tailscale+OpenSSH backdoor that outlived his C2. The lesson for embedded engineers: car hacking starts in the IT office."
tags: ["car hacking", "automotive security", "Embedded Security", "Threat Intelligence", "persistence", "supply chain"]
tagSlugs: ["car-hacking", "automotive-security", "embedded-security", "threat-intelligence", "persistence", "supply-chain"]
featured: false
image: "/content/images/2026/06/car-hacking-20260618-131725.webp"
imageAlt: "car hacking — featured image"
metaTitle: "Car Hacking Starts in IT: French Automotive Breach"
---

Real-world **car hacking** rarely starts at the CAN bus. It starts at a finance workstation in an automotive supplier's IT office, two buildings away from the bench where someone flashes an ECU. A French-speaking attacker just gave us a textbook example: he broke into a small French automotive business this June, dropped a keylogger, harvested banking and email credentials, and then did one thing that elevates this from "another small-business breach" into a teaching moment for everyone who works on vehicles. Before his command-and-control server went dark, he installed [Tailscale](https://tailscale.com/) and OpenSSH on a victim machine and built a second way in that did not route through his C2 at all. When the Havoc server [went offline the next day](https://thehackernews.com/2026/06/junior-hacker-used-tailscale-and.html), he still had a door.

If you build embedded systems for a living, your first instinct is probably "that's an IT problem, not a car hacking problem." That instinct is exactly the blind spot real adversaries are pricing into their playbooks. The bridge from a compromised finance workstation to the bench where someone flashes an ECU is shorter than most embedded engineers think, and the tradecraft on display in this breach is the tradecraft that gets used against automotive suppliers all day, every day.

This post walks through what the attacker actually did, why his persistence trick is uniquely effective against automotive companies, and why the embedded engineer's compartmentalized threat model — secure the vehicle, ignore the network — leaves the most valuable IP in the building exposed.

## What Happened: A Small Automotive Supplier, A Keylogger, and a Plan B

The intrusion itself was unremarkable for the first ninety percent of the timeline. Initial access landed on a Windows workstation. The attacker deployed a [Havoc](https://github.com/HavocFramework/Havoc) C2 beacon — an open-source post-exploitation framework that has become the budget Cobalt Strike of the European underground — and started doing what financially motivated actors do: keylogging, screenshot collection, credential theft from browsers and mail clients. Banking creds and email accounts were the prize. Nothing in those first stages required any understanding of the victim's industry.

The interesting move came near the end of his dwell time. Before his Havoc server got burned (which it did, the next day), he staged a fallback. He pulled down `OpenSSH`, set it up as a service on the compromised workstation, and layered [Tailscale](https://tailscale.com/kb/1151/what-is-tailscale) on top of it. Tailscale is a commercial mesh VPN built on WireGuard. It punches through NAT, it does not require inbound firewall rules, it authenticates via an external identity provider, and to most EDR products and most network defenders, it looks like a legitimate productivity tool because for most companies it *is* a legitimate productivity tool.

The result: even after his loud, signature-rich C2 channel was killed, the attacker could SSH into the victim from anywhere, on an encrypted overlay network, using infrastructure that no one on the defending side was watching. The keylogger was the smash and grab. The Tailscale install was the safety deposit box — and the reason this story matters for anyone doing serious car hacking research.

## Why Tailscale + OpenSSH Is the Perfect Automotive Persistence Play

Pick a random automotive supplier — Tier 2, maybe Tier 1, the kind of shop that machines a bracket or writes firmware for a body control module — and look at their environment honestly. You will usually find: a small IT team stretched across factory floor and office, a mix of Windows engineering workstations and Linux build servers, ECU flashing rigs sitting on the same subnets as accounting laptops, and a security budget that gets approved annually at best. Long product lifecycles mean machines do not get refreshed. Mixed IT/OT environments mean network segmentation is aspirational. Lean security teams mean nobody has time to baseline what "normal" outbound traffic looks like.

Drop a Tailscale node into that environment and a few things happen at once. The outbound traffic is WireGuard over UDP 41641 — not blocked at most perimeters, and even if it were, Tailscale's `DERP` relays fall back to 443. There is no inbound rule to flag. The control plane runs on `tailscale.com`, which most reputational filters score as benign. EDR products that key on suspicious binaries see a signed, well-known executable. SIEM rules that look for known-bad C2 see nothing.

Now add the automotive payoff. Once the attacker is back in via Tailscale, he is not on the perimeter — he is on the LAN, sitting next to the build server that signs firmware, the engineer's laptop with the diagnostic licenses on it, the test bench with a vehicle on the lift and CAN logs being recorded to a network share. The pivot from a compromised finance machine to high-value engineering targets is a couple of `nmap` sweeps and some lateral movement. None of it requires touching the vehicle. The vehicle is the trophy, not the entry point.

This is why automotive companies are attractive targets in ways their IT teams underweight. The IP on a build server can be worth more than a year of revenue. ECU signing keys, if exfiltrated, compromise every car a manufacturer ships until the keys rotate — and key rotation in a vehicle program is a multi-year project. Patient, infrastructure-independent access is worth more in this industry than in almost any other, which is precisely why offensive car hacking curricula need to cover it.

## The Embedded Engineer's Blind Spot: You Secure the Car, Not the Company

If you spend your days fuzzing UDS sessions, reverse-engineering ECU firmware, or writing secure boot logic, you have probably built a very sharp threat model of the vehicle itself. You know which DIDs are dangerous. You know where the seed-and-key gate sits in your diagnostic stack. You have opinions about [AUTOSAR](https://www.autosar.org/standards/foundation) crypto stacks.

That threat model has a hole the size of your employer's office network. The adversary you should be modeling is not the one connecting an OBD-II dongle in a parking lot. It is the one sitting on a workstation three desks over from the engineer who has root on the build server. When that adversary owns the IT environment, every assumption your in-vehicle threat model rests on — "only authorized binaries get signed," "only authorized engineers touch the flash tooling," "diagnostic credentials are protected" — becomes negotiable.

This is the part of automotive security that the protocol-centric view of car hacking misses. CAN bus fuzzing teaches you what a malicious frame looks like once it is on the wire. It does not teach you how an attacker gets to a position where they can put one there at scale, across a fleet, persistently, without anyone noticing. The Tailscale-OpenSSH play in this French breach is a glimpse of that upstream tradecraft: how adversaries establish the patient, infrastructure-independent foothold that makes the downstream vehicle attack possible.

And it is the part that gets weaponized in the real cases. Look at the publicly disclosed automotive incidents of the last few years and the pattern is consistent: the breach starts with a phish or a supplier compromise, persists through legitimate-looking remote-access tooling, lateral-moves to engineering systems, and only *then* touches anything resembling a vehicle. The CAN bus is the last hop, not the first. Any car hacking program worth its tuition has to teach the whole chain.

## What This Breach Teaches About Real-World Automotive Threat Models

Three concrete updates to make to your mental model after reading the report on this French breach:

- **Persistence is a separate problem from initial access.** Most attacker tooling you read about in vendor reports is about getting in. The interesting question, increasingly, is what they install that does *not* look like attacker tooling. Tailscale, AnyDesk, ngrok, Cloudflare Tunnel — these are the new persistence stack. If you are responsible for any segment of an automotive network, your detection logic needs an opinion about each of them.
- **Network segmentation between IT and engineering is the highest-leverage control you are probably not enforcing.** The fantasy is an air-gapped engineering VLAN. The reality is a flat network with a VLAN tag and no enforcement at the switch. If a compromised finance workstation can reach the firmware build server on TCP 22, you have an architecture problem, not a tooling problem.
- **Your supply chain is your attack surface.** If you are a Tier 1, your Tier 2s and Tier 3s are your perimeter. If you ship to OEMs, you are someone else's perimeter. The French automotive business in this story was small. That is the point — small suppliers are the easiest path into big ones.

If you want to dig deeper into how IT compromise chains into embedded systems, our [hands-on IoT hacking course](https://lufsec.com/courses/iot-hacking) covers the firmware-side tradecraft that complements vehicle work, and the broader [Lufsec course catalog](https://lufsec.com/courses/) indexes the practitioner paths in offensive automotive and embedded security. For a curated entry into where these skill sets fit in a career, the [Lufsec blog](/) archives the long-form breakdowns we publish weekly.

## Learn the Tradecraft the Adversary Already Knows

This is exactly the gap our [hands-on Car Hacking Course](https://lufsec.com/courses/car-hacking?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=car-hacking&utm_content=primary) was built to close. It is for embedded and automotive engineers who already know the vehicle side and want to learn how real attacks chain from IT compromise into vehicle systems — not just CAN bus fuzzing in isolation, but the full adversary path: network foothold, persistence, lateral movement onto engineering infrastructure, and the pivot from a developer workstation to a flashable ECU. You will work through realistic scenarios with the same tooling and techniques used in actual automotive incidents, and you will leave with a threat model that covers the whole attack chain, not just the last hop. If you build vehicles for a living and the French breach above made you uncomfortable, this course is built for you.

*Not ready for the full Car Hacking Course? Start with our free* [*Cybersecurity Career Guide*](https://www.lufsec.com/products/digital_downloads/cyber-security-career-guide?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=car-hacking&utm_content=secondary) *— a short, practical map of where offensive automotive skills sit in a broader security career, and how to sequence the next steps from where you are today.*
