---
title: "Anchors That Don't Lift: Why IoT Firmware Analysis Keeps Hitting 2015 Kernels"
slug: "iot-firmware-analysis-kernel-lock-in"
pubDate: 2026-06-10T12:44:51.000Z
updatedDate: 2026-06-10T12:44:51.000Z
author: "Luciano Ferrari"
description: "Your router is running a Linux kernel from 2015, and the vendor can't update it even if they wanted to. Fresh research explains why — and what it means for IoT firmware analysis past the surface scan."
tags: ["iot security", "firmware analysis", "Penetration Testing", "Supply Chain Security", "Linux Kernel"]
tagSlugs: ["iot-security", "firmware-analysis", "penetration-testing", "supply-chain-security", "linux-kernel"]
featured: false
image: "/content/images/2026/06/iot-firmware-analysis-20260610-090625.webp"
imageAlt: "iot firmware analysis — featured image"
metaTitle: "IoT Firmware Analysis: Why Kernels Stay Stuck"
---

Your router is running a Linux kernel from 2015 — and the vendor can't update it even if they wanted to. That's not laziness. That's not a patching backlog. That's a supply-chain anchor, and it changes how serious **IoT firmware analysis** should be done.

A new paper on arXiv, [Anchors that Don't Lift: Understanding Supply Chain Driven Kernel Lock-In and Governance-Mediated Mitigation Strategies in SOHO Devices](https://arxiv.org/abs/2606.11175v1), puts a label on something every practitioner who has cracked open SOHO firmware already suspected: the kernel version isn't a vendor choice. It's a chipset SDK decision made years upstream, frozen into the firmware, and effectively unfixable downstream. If you've been doing IoT pen testing and wondering why the same ancient CVEs keep surfacing on different brands, this is your answer — and the reason version-number scraping consistently underdelivers as an IoT firmware analysis technique.

For testers moving past banner-grabbing, the implication matters: some of the kernel surface you're enumerating is genuinely exploitable for years to come, and some of it is a decoy that no audit checkbox will move. Knowing the difference is the difference between a report that gets actioned and a report that gets filed.

## The Kernel Time Capsule: Why Your Smart Devices Run 2015 Linux

Pull apart any consumer router, IP camera, or smart plug and there's a strong chance the kernel string in `/proc/version` belongs to a release line that mainline Linux abandoned half a decade ago. Prior audits of SOHO firmware treated this as a version-number problem: extract the kernel string, map it to known CVEs, report the gap. The arXiv research argues that approach misses the actual mechanism — and therefore misses where the exploitable surface really is.

The picture they describe matches what teardown work surfaces every time: vendors don't ship Linux. They ship a chipset vendor's Board Support Package (BSP), which happens to contain Linux, along with proprietary drivers, a tuned scheduler, vendor-specific networking stacks, and a build system that only knows how to produce images against that exact kernel tree. The kernel isn't a choice the OEM made. It's a dependency they inherited.

That's why the version is old. The chipset vendor froze it when the SoC went into mass production, and everything downstream — the OEM, the ODM, the brand on the box — built their product around it.

## Supply-Chain Anchors: How Chipset SDKs Lock Firmware in Place

The paper's core contribution is naming this as a supply-chain anchor problem. Any serious IoT firmware analysis has to account for three reinforcing layers of lock-in:

- **Technical lock-in.** The chipset SDK includes binary-only drivers (wireless PHY, hardware crypto offload, switch fabric) compiled against a specific kernel ABI. Updating the kernel breaks those drivers. Without drivers, the device is a brick.
- **Contractual lock-in.** The OEM's license to the SDK is scoped to the version of the kernel it ships against. Re-basing onto a newer tree often falls outside the support agreement, and the chipset vendor has no commercial incentive to help.
- **Economic lock-in.** The engineering cost of forward-porting vendor patches onto a modern kernel, then re-validating the entire RF stack and regulatory compliance, exceeds the margin on a $40 router. So nobody does it.

The result is what the authors call an anchor that doesn't lift: even a motivated OEM facing public CVE pressure cannot meaningfully update the kernel. They can backport selected fixes if the chipset vendor releases them. They can't move the anchor.

For penetration testers, this reframes the threat model. The vulnerable kernel isn't a bug in someone's release process. It's a structural feature of how SOHO hardware gets built. The device you're testing today, and the one shipping next quarter, and the one after that — they are all running kernels chosen years before the product existed.

## Governance Strategies That (Sometimes) Broke the Lock

The paper's second contribution is surveying where this anchor has actually been lifted, and the answers are sobering. Pure market pressure rarely works. Buyers don't see kernel versions on the box, so there's no demand signal that reaches the chipset vendor. The interventions that have produced movement are narrower:

- **Regulatory mandates with teeth.** The EU's Cyber Resilience Act and similar frameworks attach support-lifetime obligations to the brand selling the device. When the brand is on the hook for five years of security updates, it suddenly has a reason to negotiate harder with the chipset vendor — or pick a different chipset.
- **Upstream mainlining campaigns.** When chipset vendors are pushed (often by large customers, occasionally by community efforts) to mainline their drivers into the upstream kernel, the anchor weakens. Once a driver is in mainline, the OEM can ride newer kernels without losing functionality.
- **Tiered SDK economics.** A few chipset vendors have started offering long-term-support SDK branches as a premium product. It's an admission that the default model produces unfixable devices, and it confirms that the lock-in is a commercial choice, not a physical constraint.

None of these are common. Most SOHO firmware in the wild still rides the original anchor. But the existence of the exceptions is useful intel: when you see a device running a relatively modern kernel against a known-locked chipset, that's a signal worth digging into during a teardown.

## IoT Firmware Analysis Beyond Version Numbers: Finding the Real Attack Surface

Here's where the research connects to how you should be working. If kernel lock-in is structural, then practitioner-grade IoT firmware analysis cannot stop at `strings | grep Linux`. It has to map which parts of the image are anchored and which are genuinely under OEM control.

A workable triage looks roughly like this:

- **Extract the filesystem.** Unpack the firmware image — [binwalk](https://github.com/ReFirmLabs/binwalk) for the first pass, manual carving for the cases where it can't. You're looking for a SquashFS root, the kernel blob, and any secondary partitions (config, web UI, vendor overlays).
- **Identify chipset SDK artifacts.** Kernel module names, proprietary blobs in `/lib/modules`, vendor-specific init scripts under `/etc/init.d`, and any `wl.ko`, `rt_wifi`, `mt76`, `qcawifi`, or similar markers tell you which silicon family you're inside and therefore which SDK lineage anchors the kernel.
- **Separate locked from patchable surface.** The kernel itself, the wireless drivers, the hardware crypto, the switch driver — locked. The userland web UI, the upstream BusyBox, the OEM's management daemon, the SSL stack if it's not vendor-modified — patchable, and where you should expect to see active CVE churn.
- **Validate against running hardware.** Static IoT firmware analysis lies. Pull UART, drop into the bootloader, dump live memory, and confirm what's actually loaded. The anchored kernel surface is where long-lived exploits live, but the patchable userland is where new vulns appear between firmware releases.

Done well, this gives you a report that distinguishes vulnerabilities the vendor can fix from vulnerabilities the vendor cannot fix without changing chipsets. Both are real findings. They lead to very different remediation conversations.

The version-number scrape misses all of this. It produces a list of CVEs, none of which the vendor will close, and a customer who tunes out by the third report. The supply-chain-aware IoT firmware analysis produces a prioritization the customer can actually act on.

## Where to Build This Skill Hands-On

Understanding kernel lock-in is conceptual. Finding it on real hardware is a craft. You need to be comfortable with UART pinout discovery, SPI flash dumping, firmware unpacking against uncooperative formats, and reading vendor BSPs to recognize the SDK fingerprint. Our [firmware teardown notes on the LufSec blog](/) sketch the workflow, and the wider [LufSec training catalogue](https://lufsec.com/) places the IoT track in context with the rest of the practitioner program. For testers who want a structured path into the topic, our [courses overview](https://lufsec.com/courses) is the right starting point.

That's what [**LufSec's IoT Hacking Deep Dive**](https://lufsec.com/courses/iot-hacking) is built for. It's the course for the practitioner who has already done basic IoT pen testing, who wants to stop generating reports the vendor ignores, and who is ready to work on real devices — extracting firmware, identifying chipset SDK artifacts, separating anchored surface from patchable surface, and writing findings that survive a remediation review.

If you're at the point where the arXiv paper above resonated rather than confused, you're the audience. [Take a look at the IoT Hacking Deep Dive syllabus](https://lufsec.com/courses/iot-hacking) and see if it matches where you want your IoT firmware analysis work to go next.
