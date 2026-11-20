---
title: "Microsoft, the FAA, Chase, Apple, NSA: Was This Week's Outage Wave a Cyberattack?"
slug: "outage-week-cyberattack-explained"
pubDate: 2026-11-20T12:30:00-05:00
author: "Luciano Ferrari"
description: "Six major outages in one week, and the US cyber chief is out. Officials say it wasn't an attack. A 20-year security pro explains what really broke, and why."
tags: ["Cybersecurity", "Outages", "Patch Management", "AI Security", "National Security", "Incident Response"]
tagSlugs: ["cybersecurity", "outages", "patch-management", "ai-security", "national-security", "incident-response"]
image: "/content/images/2026/11/outage-week-systemic-fragility.webp"
imageAlt: "Systemic Fragility: Luciano Ferrari on the outage wave"
---

In one week, Microsoft went down. Air traffic stopped nationwide. Chase customers couldn't pay. Apple broke. A classified NSA network went dark. Then the person in charge of America's cyber strategy left the job.

Naturally, everyone asked the same question: was this a cyberattack?

Officials say no. I've spent more than 20 years in security, so let's walk through it calmly: what happened, what didn't, and the part most coverage skipped.

<div class="embed"><iframe src="https://www.youtube-nocookie.com/embed/KgeZsq_pmp4" title="Was this week's outage wave a cyberattack?" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture"></iframe></div>

## The National Cyber Director Is Out

Sean Cairncross, the White House National Cyber Director, is leaving. He'd held the role since August 2025. The job advises the President on cybersecurity and coordinates cyber strategy across the federal government.

Accounts of his exit differ. Axios reported he chose to leave on good terms, timed so a successor could be confirmed before the Senate changes hands in January. Other reporting says he was fired. Either way, his replacement is Kirsten Davies, currently the Defense Department's Chief Information Officer.

## The Timeline: Six Outages in Six Days

- **Nov 12, Microsoft 365:** Outlook and Teams went down in the middle of the workday. Microsoft blamed a network capacity upgrade.
- **Nov 13, FAA:** A nationwide ground stop lasted more than four hours. It was tied to a contractor swapping copper for fiber at a radio facility, and more than 9,000 flights were cancelled.
- **Nov 16, JPMorgan Chase:** Payment failures from a software bug in on-premises hardware systems.
- **Nov 16, United:** Departures were held for about 1 hour 40 minutes because of a problem in the system that calculates takeoff weight.
- **Nov 17, Apple:** iCloud, Apple Pay and the App Store were hit. Apple blamed an internal update.
- **Nov 17, NSA:** A classified network went down during what officials called scheduled maintenance.

## So, Was It an Attack?

Every company involved said no. Government officials agreed:

- Homeland Security Secretary Markwayne Mullin said he's 98% confident this wasn't malicious foreign activity.
- Secretary of State Marco Rubio said there is zero evidence the outages are connected.
- Senator Mark Warner, a Democrat, also saw no sign of an attack.

When both parties agree, take it seriously. But "not an attack" doesn't mean nothing is wrong.

## The Part Most Coverage Skipped

The Director of National Intelligence tied the NSA outage directly to patching, specifically to fixing a serious flaw in PHP, which runs a huge share of the web. AI tools are now finding serious flaws in it.

Senator Warner said AI finds vulnerabilities at unprecedented speed. That's true, and it puts pressure on organizations to patch immediately, often all at once.

Speaking as a practitioner: patching isn't free. Every patch is a change to a live system. Rush it, with no staged rollout, no testing and no rollback plan, and that's how you break things.

**AI has flipped the old problem.** We used to worry that attackers found bugs faster than we did. Now defenders find them faster than they can safely fix them.

To be clear about the record: only the NSA outage has been tied to patching. The other companies gave their own causes. But the pressure is real, and officials say more patching is coming.

## What This Means for You

If you run systems:

- **Stage your rollouts.** Patch a small group first, watch it, then expand.
- **Have a rollback plan** before you patch, not after it breaks.
- **Prioritize.** Not every AI-found bug is critical. Patch what's actually exploitable first.
- **Separate patch windows** for systems that depend on each other, so one bad change doesn't take down the whole chain.

Fast and safe aren't opposites. Doing both is the skill.

## What I'm Watching

- How Kirsten Davies handles the transition
- Final root causes from the FAA and Apple
- Whether this patching wave keeps causing outages

AI finding vulnerabilities is exactly what I teach, from both the attacker's side and the defender's.

🛡️ **Free: the LLM Security Cheat Sheet.** It covers the prompt-injection and AI-agent attacks every defender should know, on one page: [Get it here](https://www.lufsec.com/products/digital_downloads/llm-security-cheat-sheet?utm_source=lufsec-blog&utm_medium=blog-cta&utm_campaign=ai-security&utm_content=outage-week)

<div class="cta"><p>🔥 Black Friday opens Tuesday, Nov 24</p><p>Every LufSec course is discounted, and there are 10 seats in my live Hacking AI Agents mentorship. Get on the list first.</p><a class="btn" href="https://black.lufsec.com/?utm_source=blog&utm_medium=post&utm_campaign=black-friday-2026&utm_content=outage-week">Join the Black Friday List</a></div>

Did any of these outages hit you this week? Tell me in the [YouTube comments](https://youtu.be/KgeZsq_pmp4).
