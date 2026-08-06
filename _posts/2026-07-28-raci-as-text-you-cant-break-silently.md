---
title: "RACI as Text You Can't Break Silently"
standfirst: "A spreadsheet cannot tell you the matrix is broken. A rule can — and it fails the check the moment a row has two Accountables."
description: "Why RACI matrices rot six months into a project, and what changes when the matrix is a YAML file with a one-Accountable-per-row rule enforced by a validator in a git hook or CI."
lang: en
---

You start a project, full of enthusiasm, and, as usual, create a set of project documents. You gather stakeholder information and create a RACI matrix. Time passes, the project progresses, stakeholders change — and six months later you look at the matrix, trying to find who is accountable for a particular stage, and you see two Accountables in one row. After numerous edits by different people the matrix is broken: everyone edits their own part, and no one looks at the whole row. Or worse — there is no one accountable at all: the only one moved on to another role. The matrix is completely out of touch with reality, useless, and rotten.

The most valuable thing you get from such a matrix is knowing who is accountable for each decision. The progress, and the entire outcome of the project, depend on it. It's terrible when there are two or three Accountables for a stage, and even worse when there are none.

Of course, I understand that there can be many approvers. Any of them can block a decision, but the Accountable is the one who answers for it.

When you create such a matrix in a spreadsheet, it has no mechanism to keep it in working order and validate it automatically. Simply put, no one will tell you that the matrix is broken.

I often talk about Architecture-as-Code, and in that approach it is easier to keep a document up to date, because it has rules it lives by and constraints that apply to it. It's easy to create a "One A per row" rule, and every time it's violated, validate --template raci will fail, and you will know about it.

Try the template from the repository. It's a simple YAML file, quite human-readable. Inside are the table columns and the roles you already know. Fill in your roles, activities, and assignments — and the document is ready to use. Break it on purpose: add a second A to any row and see how validation works (validate --template raci). It doesn't just print an error, it returns a non-zero exit code — so you can put it in a git hook or a CI workflow and automate the check. Copy or fork the whole transitrix/templates repository, MIT.

This is one of the two templates already in the library of forkable starters.
