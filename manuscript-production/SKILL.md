---
name: manuscript-production
description: Use this skill when helping produce a scholarly, clinical, or research manuscript from idea through submission. Trigger for manuscript planning, source packet creation, evidence matrices, outlines, drafting, claim calibration, reference audits, reviewer responses, coauthor packets, submission readiness checks, or when the user says they want to produce or supercharge manuscripts.
---

# Manuscript Production

## Operating Principle

Treat manuscript work as a production pipeline, not a sequence of disconnected edits. The user's role is direction, clinical/domain judgment, taste, and final sign-off. Codex owns decomposition, evidence organization, candidate generation, audit trails, and making uncertainty visible.

Do not let the workflow jump straight into prose unless the user explicitly asks. When the project is early, start upstream: why the paper matters, who it is for, what artifact is being built, the end goal, and how success will be measured.

## Stage Gate

Move through visible stages:

1. Brief
2. Source packet
3. Outline/options
4. Draft
5. Verify
6. Revise
7. Ship

The key gate is source packet before prose. If the user is beginning a manuscript and has not gathered references, stop and build the minimum viable source packet first. Late reference searching causes unstable claims, citation mismatch, duplicated framing, and repeated final audits.

## First Response Pattern

Classify the manuscript stage before doing work:

- Idea-stage: clarify purpose, audience, target journal, success measure, and core claim.
- Source-stage: build source packet, evidence matrix, and claim ledger before drafting.
- Draft-stage: preserve the user's voice, tighten structure, and check evidence alignment.
- Revision-stage: map reviewer comments to manuscript changes and response-letter language.
- Final-stage: audit for coauthor-ready versus submission-final status.

Ask only the questions that change the next concrete move. Prefer producing a reusable artifact over giving general advice.

## Required Artifacts

For a new manuscript, create or maintain these files in the project folder unless the user asks for another format:

- `00_brief.md`: manuscript purpose, audience, journal target, core claim, success measure.
- `01_source_packet.md`: must-read sources grouped by role.
- `02_evidence_matrix.csv`: source-by-source evidence table.
- `03_claim_ledger.md`: major claims and support level.
- `04_outline.md`: section-level argument plan.
- `05_reviewer_tracker.md`: reviewer comments, response status, and manuscript locations.
- `06_reference_audit.md`: citation/reference issues and exact fixes.
- `07_final_readiness.md`: coauthor-ready and submission-final dashboard.

Templates are in `assets/`. Copy and adapt them when starting a project.

## Evidence Discovery Tools

For clinical manuscripts, use evidence-discovery tools during the source-packet stage, not after drafting. If an OpenEvidence MCP server is available, it can help ask focused clinical questions, retrieve prior OpenEvidence article payloads or history, and generate candidate sources for the source packet.

Use OpenEvidence-style results as evidence leads, not final citation authority. Verify important claims through full text, PubMed/journal pages, guidelines, or the user's source library before drafting strong claims. Record useful leads in `01_source_packet.md` and convert verified sources into `02_evidence_matrix.csv`.

If OpenEvidence MCP is not configured, continue with PubMed, journal sites, guidelines, PDFs, Zotero exports, and local source folders.

## Claim Discipline

For clinical/research manuscripts, prioritize source fidelity, conservative claims, full-text evidence, measurable outcomes, and human review.

Classify major claims as:

- Established: directly supported by strong evidence or consensus.
- Associated: supported by observational or correlational evidence.
- Plausible: biologically or mechanistically reasonable but not proven.
- Hypothesis-generating: suggestive, incomplete, or exploratory.
- Overclaimed: stronger than the evidence supports.

When a claim is clinically useful but not definitively proven, preserve usefulness without overstating certainty. Prefer language such as "may," "is associated with," "is clinically actionable," "supports evaluation," or "remains an open research question" when appropriate.

## Drafting Rules

- Preserve the user's voice and current prose unless asked to rewrite from scratch.
- Make local edits when the existing argument is sound.
- Keep reviewer defensibility ahead of polish.
- Avoid duplicated rationale across Introduction, Discussion, and Conclusion.
- Track word debt early; do not wait until final submission.

## Verification Rules

Before any serious audit, use the current saved manuscript file, not an older export or stale extraction. Re-extract current DOCX text after each edit cycle before trusting prior notes.

For near-final clinical manuscripts, check:

- reviewer-response alignment
- claim strength versus evidence strength
- citation/reference integrity, including possible hidden citation field residue
- word count and journal fit
- figure/table consistency
- coauthor-ready versus submission-final status

If giving corrections, prefer exact Markdown deliverables:

- `Find ...`
- `Replace with ...`

For sentence-level work, show only the current lines that need replacement unless broader context is necessary.

## Automation Helpers

Scripts in `scripts/` are intentionally small and project-agnostic:

- `extract_docx_text.py`: extract text and visible references from a DOCX.
- `manuscript_word_count.py`: estimate section-level word counts from a text extraction.
- `risky_claim_scan.py`: flag potentially overstrong clinical/research language.

Use these as intake helpers, then apply judgment. Script output is not a substitute for source review or user sign-off.

## Common Failure Modes

- Searching for references only after drafting: fix by building `01_source_packet.md`, `02_evidence_matrix.csv`, and `03_claim_ledger.md` before prose.
- Clean-looking bibliography but persistent citation issues: fix by re-extracting the current DOCX and checking hidden/stale citation residue.
- Generic audit that does not answer the real risk question: fix by explicitly saying coauthor-ready, submission-final, or not ready.
- Clinical-actionability framing becomes causal overclaiming: fix by tying claims to the evidence level and naming what remains unproven.
- Late audit keeps reopening the whole paper: fix by narrowing to the stable blocker set once the argument is settled.
