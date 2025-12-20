# Code Review Verification Prompt (v2)

> **Version:** 2.0
> **Purpose:** QA verification review after fixes are implemented
> **Use Case:** Run this prompt with multiple LLMs (Claude, GPT, Gemini, etc.) to get comprehensive verification coverage

---

## Prompt

```
Remember <nickname> YYYY

Remember the <branch_name> XXXXXXX
Remember <module_name> ZZZZZZ

Act as a **Senior Quality Assurance Lead** and **Code Review Verifier** with 15+ years of experience in the Frappe Framework. Your primary objectives are:

1. **Verify** that all fixes outlined in the Master Fix Plan have been correctly implemented
2. **Detect regressions** — new bugs, security issues, or architectural violations introduced BY the fixes
3. **Discover new issues** — problems that were MISSED in the original review (fresh eyes review)
4. **Preemptively flag** issues that GitHub Copilot's automated review would flag

---

### Output Instruction
Store your final verification and updated code review in the existing file named **<nickname>_review_v2.md** in the existing folder **specs/<branch_name>/review/**, substituting in the remembered terms. Note the version of this file clearly at the top. Update the version as Pass 1 and Pass2 etc each time this file is updated from another review.

---

**The Context for Verification:**
* **Project/Branch:** <branch_name>
* **Reference Documents (REQUIRED READING):**
  1. **MASTER_PLAN.md:** The source of truth detailing the issues that were *intended* to be fixed.
  2. **dartwing_core_arch.md:** The project's architectural standards.
  3. **dartwing_core_prd.md:** The feature's functional requirements.
* **The Code Block to Review:** All committed changes in this branch <branch_name> (the changes implemented after the MASTER_PLAN).

---

**Your Review MUST be organized into the following five distinct sections:**

### 1. Fix Verification (Severity: CRITICAL)

* **Verification Status:** Systematically check every P1 and P2 item listed in the **MASTER_PLAN.md**. For each item, state whether the fix was **[SUCCESSFULLY IMPLEMENTED]** or **[FAILED/INCORRECT]**.
* **Evidence Required:** For each fix, cite the specific file and line number where you verified the implementation.
* **Action:** For any failed fix, explain **why** it failed and provide a precise, line-by-line **fix suggestion**.

---

### 2. Regression Check (Severity: CRITICAL)

* **Goal:** Identify any **new bugs, security issues, or architectural violations** that were **accidentally introduced while implementing the fixes**.
* **Focus Areas:**
  * Did any fix break existing functionality?
  * Did any fix introduce new edge cases that aren't handled?
  * Did any fix create inconsistencies with other parts of the codebase?
  * Are there any new race conditions, null pointer issues, or exception handling gaps?
* **Action:** For each regression found, provide **file:line**, explain the issue, and suggest a fix.

---

### 3. Fresh Code Review — New Issues Discovery (Severity: HIGH)

* **Goal:** Conduct a **fresh review of all changed files** to find issues that were **MISSED in the original v1 review**. Assume the original reviewers may have overlooked something.
* **Approach:**
  * Re-read each modified file as if seeing it for the first time
  * Look for issues NOT already documented in MASTER_PLAN.md
  * Check for logic errors, edge cases, security gaps, performance issues
* **Focus Areas:**
  * **Input validation gaps:** Are all API parameters validated? What happens with null/empty/malformed input?
  * **Error handling:** Are all exceptions caught appropriately? Are error messages safe (no info leakage)?
  * **Security:** SQL injection, permission bypasses, sensitive data exposure, missing auth checks
  * **Edge cases:** Empty arrays, boundary conditions, concurrent access, cache invalidation
  * **Code correctness:** Off-by-one errors, incorrect boolean logic, type mismatches
* **Action:** For each new issue found, classify severity (P1/P2/P3), provide **file:line**, and suggest a fix.

---

### 4. Preemptive GitHub Copilot Issue Scan (Severity: MEDIUM)

* **Goal:** Identify and address common issues that an LLM-based review agent on GitHub.com would flag, clearing the path for a quick PR approval.
* **Focus Areas:**
  * **Code Smells/Complexity:** Flag highly complex functions (e.g., high cyclomatic complexity, deeply nested logic, methods > 50 lines)
  * **Docstring/Type Hinting:** Ensure all public Python functions have accurate docstrings and type hints
  * **Security Pattern Check:** Hardcoded secrets, unchecked user input, insecure uses of built-in functions
  * **Dead Code:** Unused variables, unreachable code, commented-out blocks
  * **Test Quality:** Flaky tests, missing assertions, overly broad exception handling
* **Action:** Provide immediate, actionable **fixes** for these issues so they can be resolved directly in VS Code before the PR is created.

---

### 5. Final Summary & Sign-Off (Severity: LOW)

* **Fix Verification Summary:** X/Y P1 fixes verified, X/Y P2 fixes verified
* **Regressions Found:** List count and severity
* **New Issues Found:** List count and severity (these should be added to a follow-up fix plan if blocking)
* **Copilot Issues:** List count and whether addressed
* **One-paragraph final summary** of the branch's quality, stating the overall success rate and any remaining high-level concerns.
* **Sign-Off:** If all P1/P2 items from the original plan are verified correct AND no P1 regressions/new issues were found, state clearly: **"FINAL VERIFICATION SIGN-OFF: This branch is ready for final QA and merging."**
* **Conditional Approval:** If P2/P3 new issues were found but no P1 blockers, state: **"APPROVED WITH FOLLOW-UP: Branch can merge, but the following issues should be addressed in a subsequent PR: [list]"**

---

**CRITICAL CONSTRAINTS:**

1. **Balance verification with discovery:** Spend roughly equal effort on (a) verifying known fixes and (b) finding new issues
2. **Fresh perspective:** When reviewing for new issues, pretend you have NOT read the MASTER_PLAN — what would you flag?
3. **Be specific:** Every issue must have file:line references and concrete fix suggestions
4. **Prioritize correctly:** A P1 regression or new P1 issue is a BLOCKER even if all planned fixes are correct

---

**Post back to the console the verification status of the highest priority item from the MASTER_PLAN.md, PLUS any P1/P2 new issues discovered.**
```

---

## Usage Instructions

### Step 1: Prepare Reference Documents
Ensure the following files exist in your branch:
- `specs/<branch_name>/review/MASTER_PLAN.md` (or `MASTER_REVIEW.md` / `FIX_PLAN.md`)
- `docs/dartwing_core/dartwing_core_arch.md`
- `docs/dartwing_core/dartwing_core_prd.md`

### Step 2: Run with Multiple Models
Run this prompt with different LLMs to get diverse perspectives:

| Model | Nickname | Strengths |
|-------|----------|-----------|
| Claude Opus 4.5 | opus45 | Deep reasoning, architectural compliance |
| Claude Sonnet 4.5 | sonn45 | Balanced speed/quality, good pattern detection |
| GPT-4.5 | GPT52 | Fresh perspective, finds missed issues |
| Gemini 3.0 | gemi30 | Different viewpoint, catches edge cases |

### Step 3: Synthesize Results
After running all models, create or update `MASTER_REVIEW.md` to incorporate:
- All verified fixes
- Regressions found by any model
- New issues discovered by any model
- Consensus on sign-off status

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2025-12-16 | Added Section 2 (Regression Check), Section 3 (Fresh Code Review), conditional approval, explicit constraints |
| 1.0 | 2025-12-14 | Initial version - fix verification and Copilot scan only |

---

## Key Differences from v1

| Aspect | v1 Prompt | v2 Prompt |
|--------|-----------|-----------|
| Regression check | Buried in Section 1 | **Dedicated Section 2** |
| Finding new issues | Implicit/optional | **Explicit Section 3** with checklist |
| Sign-off options | Binary (approved/not) | **Conditional approval** option |
| Output structure | 4 sections | **5 sections** with clear separation |
| Constraints | None explicit | **4 critical constraints** listed |
| Balance guidance | None | **Equal effort** on verify vs. discover |
