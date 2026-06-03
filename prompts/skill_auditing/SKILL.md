# Skill Audit Framework

## Purpose

This audit framework is used to review, optimize, and improve
existing Claude skills, workflows, and automation logic.

The audit should focus on:

* maintainability
* deterministic execution
* composability
* safety
* reusability
* operational simplicity
* reduced manual work

---

# Audit Instructions

Audit all existing skills for the following areas:

## 1. Visibility & Safety

Identify skills with potentially dangerous side effects such as:

* deployment
* infrastructure modification
* repository changes
* automatic commits
* message sending
* production writes

Suggest whether these skills should require:

* explicit confirmation
* manual invocation only
* restricted execution behavior

Also identify skills that should remain hidden background utilities
instead of user-facing operational skills.

---

## 2. Deterministic vs Non-Deterministic Logic

Find any workflow step where AI reasoning is being used
for a fixed, repeatable operation.

Examples:

* folder creation
* environment setup
* dependency installation
* repository bootstrapping
* file generation
* naming normalization
* formatting operations

Suggest replacing these steps with:

* reusable scripts
* templates
* helper utilities
* deterministic automation logic

AI reasoning should remain focused on:

* architecture decisions
* tradeoff analysis
* debugging
* planning
* research
* documentation
* business interpretation

---

## 3. Composability & Reusability

Identify:

* duplicated logic
* overlapping responsibilities
* repeated implementation patterns
* reusable abstractions

Suggest:

* extracting shared logic
* creating helper utilities
* creating smaller reusable skills
* improving modularity

---

## 4. Verification & Validation

Check whether skills include:

* validation steps
* verification logic
* output consistency checks
* deployment verification
* configuration validation
* error handling guidance

Identify missing verification opportunities.

---

## 5. Workflow Optimization

Identify areas where the user repeatedly performs:

* manual checking
* validation
* copy/paste workflows
* repetitive setup tasks
* repeated prompting
* environment configuration
* repository initialization

Suggest reusable automation or skill improvements.

---

# Output Format

For every audit:

1. Identify the issue
2. Explain why it is problematic
3. Suggest the improved approach
4. Estimate productivity or reliability improvement
5. Suggest whether:

   * a new skill
   * a reusable script
   * a shared utility
   * or a CLAUDE.md rule

should be introduced.

Always prefer:

* simplicity
* maintainability
* operational clarity
* reusable automation
* deterministic execution
