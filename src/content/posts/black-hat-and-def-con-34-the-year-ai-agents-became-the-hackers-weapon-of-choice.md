---
title: "Black Hat and DEF CON 34: The Year AI Agents Became the Hacker's Weapon of Choice"
slug: "black-hat-and-def-con-34-the-year-ai-agents-became-the-hackers-weapon-of-choice"
pubDate: 2026-08-10T13:19:40.000Z
updatedDate: 2026-08-10T13:19:40.000Z
author: "Luciano Ferrari"
description: "AI agents went from novelty to standard hacking weapon this year. My on-the-ground recap of Black Hat and DEF CON 34 — the AI bootcamp, the villages, 16 interviews, and the launch of Inside Cyber Minds Season 3."
tags: []
tagSlugs: []
featured: true
image: "/content/images/2026/08/bhdc2026.webp"
---

*Four days of AI training, a week in the villages, and 16 conversations with the people shaping cybersecurity, plus the launch of Inside Cyber Minds Season 3.*

---

I just got back from a week in Las Vegas covering [Black Hat USA](https://blackhat.com/us-26/) and [DEF CON 34](https://defcon.org/html/defcon-34/dc-34-index.html) as press for LufSec, and I'm still processing everything I saw. This was my most ambitious Hacker Summer Camp yet: four days deep in an [AI Cyber Bootcamp](https://gtkcyber.com/lp/ai-cyber-bootcamp-black-hat-2026/), days spent walking the [DEF CON villages](https://defcon.org/html/defcon-34/dc-34-villages.html), and, the part I'm most excited about, sitting down with 16 of the sharpest minds in the industry for a brand-new season of the Inside [Cyber Minds podcast](https://www.youtube.com/playlist?list=PLSduWfD6T_1ESuTU4eQwjf6MKOXpZjwPM).

If there was one message written across both conferences this year, it was this: **AI agents have graduated from novelty to standard hacking weapon.** Let me walk you through what I saw, what it means for practitioners, and who you'll be hearing from all season long.

## The Theme That Defined Hacker Summer Camp 2026

Every year, Hacker Summer Camp has a center of gravity. This year it was impossible to miss.

At Black Hat, nearly every keynote and a huge share of the Briefings centered on AI. Offensive tradecraft, AI-assisted vulnerability discovery, and the uncomfortable question the whole industry is now wrestling with: *what happens when AI starts doing the attacking?* Attackers are already using AI to find and chain vulnerabilities faster than most teams can patch them, and the research on stage reflected a field racing to keep up.

DEF CON 34 took it further. [Jeff "The Dark Tangent" Moss](https://defcon.org/html/defcon-34/dc-34-speakers.html) framed the entire conference around the theme of **"Agency"**,self-determination in an era of algorithmic manipulation, dark patterns, and shrinking digital autonomy. The AI Village's debut HALctf competition formalized autonomous pentesting as a discipline, with competitors building AI agents, packaging them as containers, and deploying them against sandboxed targets. The message from the village was refreshingly blunt: strip away the hype and focus on practical, hands-on AI security.

The attack surface has quietly expanded from "networks and servers" to cars, satellites, medical implants, and now the AI agents doing the hacking themselves. That shift shaped everything I did this week.

## Four Days in the AI Cyber Bootcamp

Before the villages opened, I spent four days as a student in [GTK Cyber's AI Cyber Bootcamp](https://gtkcyber.com/lp/ai-cyber-bootcamp-black-hat-2026/) at Black Hat, and even after 20+ years in this field, I'm a firm believer that the day you stop being a student is the day you fall behind.

It's a genuinely comprehensive four days, moving from machine learning foundations for security through generative AI and LLMs, building AI agents for triage and automation, and into adversarial AI, hands-on evasion, poisoning, prompt injection, and RAG poisoning, along with the defenses. Half the time is labs, so you leave with working code rather than just slides. What struck me most was the shift in the room compared to a year ago. "AI security" used to feel speculative. This year, everyone in that bootcamp understood it was already their job; they were there to sharpen skills they now use in anger. Sitting on the student side of the table, working through the exact adversarial techniques that the rest of the week would go on to prove were urgent, was exactly the kind of alignment that made Hacker Summer Camp worth the trip.

<figure><img src="/content/images/2026/08/ChatGPT-Image-Aug-9--2026--08_56_40-AM.webp" alt="" loading="lazy" /></figure>

> **Want to go deeper on the technique everyone's talking about?** Prompt injection came up in the bootcamp and echoed throughout both conferences all week; it's the single most-referenced AI attack technique in the industry right now. My new course, [**Prompt Hacking for LLMs: Intro**](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro), takes you hands-on through how these attacks actually work and how to defend against them. **To celebrate the launch of Season 3, use code `SUMMERCAMP40` for 40% off through August 14th.** [Claim 40% off →](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro)

## Walking the DEF CON Villages

The villages are the beating heart of DEF CON, and this year I focused my time across the ones closest to LufSec's work. Here's what stood out.

### Maritime Hacking Village

Maritime cyber has been a personal focus of mine, and the Maritime Hacking Village continues to punch above its weight. The conversations here weren't abstract; they were about the real attack surface on real vessels: GNSS and AIS spoofing, bridge systems, and the human decisions that lead to how ships get compromised. If you think the maritime domain is too obscure to matter, you haven't been paying attention to how much of the global economy floats.

<figure><img src="/content/images/2026/08/maritimevillage.webp" alt="" loading="lazy" /></figure>

### Aerospace Village

The Aerospace Village brought some of the most striking research of the week, including practical, real-world message attacks against aircraft communications systems. Watching researchers demonstrate spoofing against certified avionics using accessible software-defined radio gear was a sharp reminder that safety-critical infrastructure still leans far too heavily on "nobody will try this."

### Car Hacking Village

The Car Hacking Village ran a CTF on live vehicle architectures, and the pace of automotive security research continues to accelerate. From CAN bus manipulation to the sprawling attack surface of dealer portals and connected-car backends, this village makes one thing clear: the modern car is a computer network on wheels, and it's being probed accordingly.

### IoT Village

The IoT Village remains one of the most consistently eye-opening stops at DEF CON. Year after year, its research and CTF surface the same uncomfortable truth: the connected devices filling our homes, offices, and critical infrastructure are riddled with the kinds of flaws we thought the industry had left behind a decade ago. Hundreds of CVEs have come out of this village over the years, and walking the floor this year, it's obvious the pipeline of vulnerable devices isn't slowing down. If anything, adding AI and more connectivity to everything has widened the target.

### Red Team Village

The Red Team Village remains one of the best places at DEF CON to see offensive tradecraft evolve in real time. This year the AI thread ran straight through it. Red team agents, autonomous tooling, and the growing question of how human operators work alongside AI without losing the craft.

### Recon Village

Recon Village was a highlight for me this year. The OSINT and reconnaissance community is grappling with the same AI tension as everyone else: automation makes collection faster, but the human analysis layer, reading the motivations and signals behind the data, is what still separates good intelligence from noise. Some of the best conversations of my week happened here.

### AppSec Village

And the AppSec Village grounded all the AI excitement in something practical: the application security fundamentals that don't go away just because there's a language model in the pipeline. Supply chain risk, dependency security, and the reality that AI systems inherit every weakness of the CI/CD pipelines and identity layers they're built on.

## The Real Reason I Was There: The Interviews

Here's the truth: I spent most of my week not watching talks, but recording them. My mission this year was to bring the voices of Hacker Summer Camp directly to the LufSec community, and that meant sitting down, mic in hand, with as many brilliant people as I could.

I'm humbled to say I landed **16 interviews** across Black Hat and DEF CON, with researchers, tool creators, village leaders, and some of the most recognizable names in the industry. Every one of them generously gave me their time in the middle of the security calendar's busiest week, and I couldn't be more grateful.

These conversations became something bigger than I planned. **They are now Season 3 of Inside Cyber Minds.**

## Announcing Inside Cyber Minds — Season 3

**Season 3 of Inside Cyber Minds launches this Wednesday**, and new episodes drop every Wednesday after that.

This is a special season recorded entirely on the ground at Black Hat and DEF CON 34, but a smaller 15-minute version, instead of my regular ~1-hour interview. Each episode follows the same tight structure: past, present, and future, as I ask each guest how they got into security, what they're building and breaking right now, and where they see their corner of the field heading. The lineup spans AI agent security, bug bounty and recon, automotive and aviation hacking, maritime cyber, cloud, threat intelligence, physical security, and the story of running the wildest network on earth.

I'm keeping the full guest list as a running reveal throughout the season, but expect conversations with people behind the tools you use every day, research that will shape the next 12 months, and perspectives you won't hear anywhere else.

**Subscribe on the** [**LufSec YouTube channel**](https://www.youtube.com/@lufsec) **and wherever you get your podcasts so you don't miss an episode.** First one drops Wednesday.

## Thank You to Everyone Who Sat Down With Me

None of this happens without the guests. To every researcher, founder, village leader, and operator who took 15 minutes out of the most chaotic week of the year to talk with me. Thank you! Your generosity is the entire reason this season exists, and I can't wait for the community to hear what you shared.

To the DEF CON press team and the village organizers who made space for this coverage: thank you for the trust and the access.

And to the LufSec community, this season is for you. Hacker Summer Camp only comes once a year, but the ideas that came out of it will carry us forward for months.

## What This Year Taught Me

If I had to distill a week of Black Hat and DEF CON 34 into a single takeaway, it's this: **the tools are changing faster than the defenses, and AI is now on both sides of every engagement.** The autonomous agent probing your infrastructure and the autonomous agent defending it are running the same playbook at machine speed. The practitioners who thrive from here won't be the ones who fear that shift; they'll be the ones who understand it, get hands-on with it, and stay curious enough to keep learning.

That's what LufSec is here to help you do. If AI security is where you want to level up, the fastest place to start is understanding how attackers manipulate large language models in the first place. My new course, [**Prompt Hacking for LLMs: Intro**](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro), takes you hands-on through the exact prompt injection techniques dominating the conversation at Black Hat and DEF CON this year, and how to defend against them. **Use code `SUMMERCAMP40` for 40% off through August 14th.** [**Enroll now →**](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro)

And starting Wednesday, Season 3 of Inside Cyber Minds will bring you the people leading the way.

See you Wednesday.

---

*Luciano Ferrari is the founder of LufSec and host of the Inside Cyber Minds podcast. LufSec provides practitioner-focused cybersecurity training in offensive security, penetration testing, AI security, and more. Get hands-on with AI attacks in the new* [*Prompt Hacking for LLMs course*](https://www.lufsec.com/products/courses/prompt-hacking-for-llms-intro) *— 40% off with code `SUMMERCAMP40` through August 14th. Explore the full catalog at* [*lufsec.com*](https://lufsec.com/) *and subscribe on* [*YouTube*](https://www.youtube.com/@lufsec)*.*
