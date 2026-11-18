---
title: "Who's Watching Your AI Agent? Kyle Quest on Sandboxing, eBPF, and Security Through Less"
slug: "kyle-quest-dockerslim-ai-agent-sandboxing-ebpf"
pubDate: 2026-11-18T09:00:00-05:00
author: "Luciano Ferrari"
description: "AI coding agents run commands and touch your credentials. DockerSlim creator Kyle Quest on reverse engineering agents, eBPF sandboxing, and less is more."
tags: ["AI Security", "Container Security", "Podcast", "Inside Cyber Minds", "DevSecOps"]
tagSlugs: ["ai-security", "container-security", "podcast", "inside-cyber-minds", "devsecops"]
image: "/content/images/2026/11/kyle-quest-thumbnail.webp"
imageAlt: "Kyle Quest on Inside Cyber Minds"
draft: false
---

A year ago, the scariest thing on most developer laptops was an outdated dependency. Today it might be the AI coding agent with permission to run shell commands, read every file in the repo, and use whatever credentials happen to be sitting in the environment.

That shift is what I wanted to dig into with Kyle Quest, creator of DockerSlim (now SlimToolkit), in the latest episode of Inside Cyber Minds. We recorded it onsite at DEF CON. Kyle has spent two decades working security from every side, as a builder, a breaker, and a defender. Lately he has been reverse engineering AI coding agents to understand what they actually do when you hand them the keys.

<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/snJwjGA-sW0" title="Inside Cyber Minds with Kyle Quest" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

**▶️ Watch the full episode:** [Inside Cyber Minds with Kyle Quest on YouTube](https://www.youtube.com/watch?v=snJwjGA-sW0)

## Security Through Less

To understand how Kyle thinks about AI agents, start with the project that made his name.

Most container images ship with far more than the application needs: shells, package managers, debugging utilities, libraries nobody calls. Every one of those is something an attacker can use once they're inside. DockerSlim takes a different approach. It watches what an application actually uses at runtime, then builds a much smaller image containing only that. It can also generate security profiles that restrict the container to the behavior it was observed doing.

The idea underneath is simple, and it holds up across the industry: **the most secure code is the code that isn't there.** You can't exploit a binary that was never shipped, and you can't pivot through a tool that was removed.

That idea carries straight over to AI agents. The question stops being "how do we make the agent trustworthy?" It becomes "how little does the agent actually need, and how do we make sure that's all it gets?"

## The New Untrusted Code on Your Machine

Our industry spent decades learning how to deal with code we don't fully trust. We built sandboxes for browsers, isolation for containers, least privilege for service accounts, and permission prompts for mobile apps. The lesson was always the same: assume the code might misbehave, and limit what it can reach.

AI coding agents break that pattern in an uncomfortable way. We invite them in on purpose. We give them terminal access because that's what makes them useful. They read the codebase, run the tests, install packages, and edit configuration. They make many of those decisions themselves, in ways that aren't fully predictable even to the people who built them.

That doesn't make AI agents bad. Kyle builds with them, and so do I. But it means they belong in the same category as any other powerful code running with real permissions, which is something you should understand and contain.

This is why reverse engineering matters. Documentation describes what a tool is supposed to do. Reverse engineering tells you what it actually does: which processes it spawns, which files it touches, which network connections it makes. You can't write a good sandbox policy for behavior you haven't observed.

## Why eBPF Changes the Game

A big part of our conversation was eBPF. Kyle has spoken about it at the eBPF Summit and KubeCon.

eBPF lets you run small, verified programs inside the Linux kernel. Practically, that means you can observe and control what processes do at a very low level, including system calls, file access and network activity, without modifying the applications themselves and with relatively little overhead.

For AI agent security, that matters for two reasons:

- **Visibility.** You can see exactly what an agent's processes are doing in real time, not just what the agent reports.
- **Enforcement.** You can build policies that block behavior outside an allowed profile, at a layer the agent itself can't easily get around.

Put that together with the DockerSlim philosophy and you get a clear model. Observe what the agent legitimately needs, allow that, and deny the rest.

## Container Security in 2026

We also covered where container security stands now. Containers became the default way to ship software, and with that came a familiar pattern: bloated base images, over-permissioned workloads, and runtime environments nobody fully inventories.

The good news is that the tools to fix this exist. Minimal images, runtime security profiles, and kernel-level observability are all mature. Adoption is the hard part, because doing it right takes effort and the defaults still favor convenience. Kyle's work has always been about making the secure option the easy one, and that's the right fight for AI infrastructure too.

## What's Next: AI-Native Infrastructure

We closed on the future. As AI agents move from developer laptops into production pipelines, CI systems and cloud environments, isolating them stops being a niche concern and becomes core infrastructure. The organizations that do well will treat agent sandboxing the way they treat network segmentation today: not optional, and designed in from the start rather than added after an incident.

If you work in DevSecOps, cloud security or platform engineering, this is the episode to watch this month.

**▶️ Watch the full episode:** [Inside Cyber Minds with Kyle Quest on YouTube](https://www.youtube.com/watch?v=snJwjGA-sW0)

<div class="cta"><p>🖤 Black Friday Is Coming to LufSec: Win a Flipper Zero 🐬</p><p>Join the Black Friday list free and you're entered in our Flipper Zero drawing. You also get early access to our biggest course deals of the year.</p><a class="btn" href="https://black.lufsec.com/?utm_source=blog&utm_medium=post&utm_campaign=black-friday-2026&utm_content=s3e14">Join the Black Friday List</a></div>

## Build the Skills Behind the Conversation

Understanding how attackers think about systems, and how to lock those systems down, is the foundation for working on problems like this one.

If you're just getting started, grab the **free Cyber Security Career Guide**. It covers the roles, skills, certifications, and the shortest route into the industry, and downloading it unlocks a free lesson from the LufSec course library.

👉 [Get the free Career Guide](https://www.lufsec.com/products/digital_downloads/cyber-security-career-guide?utm_source=blog&utm_medium=post&utm_campaign=career-guide-funnel&utm_content=s3e14)

Ready to get hands-on? Explore the full LufSec course catalog:

👉 [Browse LufSec courses](https://www.lufsec.com/courses/?utm_source=blog&utm_medium=post&utm_campaign=career-guide-funnel&utm_content=s3e14-course)

## Listen on Your Favorite Platform

Inside Cyber Minds is available wherever you get your podcasts: [YouTube](https://youtube.com/@Lufsec), [Spotify](https://open.spotify.com/show/6hWg94SxRjHUMCMXoKutlc), [Apple Podcasts](https://podcasts.apple.com/us/podcast/inside-cyber-minds/id1851011640), [Amazon Music](https://music.amazon.com/podcasts/87069409-9772-4c83-821a-d5607e52be51/inside-cyber-minds), and [Audible](https://www.audible.com/podcast/Inside-Cyber-Minds/B0G15CT6R1?source_code=ASSGB149080119000H&share_location=pdp).

Learn more about Kyle's work at [slimtoolkit.org](https://slimtoolkit.org/).

*Inside Cyber Minds is a cybersecurity podcast by LufSec, hosted by Luciano Ferrari. Each episode is a deep, unscripted conversation with hackers, CISOs, researchers, founders, and security leaders.*
