---
title: "Architecture-as-Code for the Enterprise — What Current EA Tools Miss"
standfirst: "Repositories of diagrams promised order and delivered folders of final-final versions. The model is data, and text is what makes it behave like data."
description: "Why enterprise architecture tools still produce documents you cannot diff, and what changes when the model is stored as text: versions, diffs, attributable changes, and an AI assistant that can actually read the architecture."
lang: en
---

Fifteen years into enterprise architecture, I keep watching the same failure pattern. You decide to tidy up your architecture documentation. Six months later, you're staring at another folder of files like `target_state_ver.2_final-prerelease_approved[DRAFT][-0.332-Albert.vsdx]`.

The textbook promised that a repository of architectural artifacts would sort everything out. It never said you can't force colleagues to follow the rules. Users hunt for the right version of every document. You can't automatically diff two Visio drawings or PowerPoint decks. Your AI assistant can't read them either.

Developers, meanwhile, have repositories: single source of truth, version control, attributable changes, every character visible. So we need a tool that treats architecture as a repository.

The diff alone gives it away. Compare two ArchiMate XML files: a wall of changed attributes. Compare two text models: you see exactly which goal moved, which capability appeared, which relationship broke.

An AI assistant reads code. In this shape it reads your architecture too — comparing, editing, eventually writing. It keeps the model current as the enterprise landscape changes.

Remember your old folder of diagrams, the one with "final-final ver. 12"? That never used to work, did it?

Architecture-as-code is the answer. The model is text — ArchiMate objects and relationships in plain files. AI shapes it and keeps it current. The same graph renders differently for a CFO, a network engineer, or an executive — each view is real, not one that's months out of date.

You stop drawing diagrams. You talk to your enterprise model.

The model is your organization's data. Versions, diffs, branches, merges, automated validation — every operation we accept on code becomes natural on the architecture too. This is what enterprise architects have been trying to achieve for the last twenty years.

That's the gap I built Transitrix to close.

If this resonates, the methodology is open source and free. Its companion tool authors and renders architecture as text in VS Code, Cursor (Windows preview), and IntelliJ IDEA, plus a skill in Claude Code. To get started, go to transitrix.com/quickstart and copy the prompt into your coding agent.
