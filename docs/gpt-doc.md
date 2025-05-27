# Fredericktown Local Schools ‑ Pro Bono Data‑Analytics Engagement

## 1. Key Concepts

| Concept                        | Description                                                                                                       |
| ------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| **Community‐driven analytics** | Donate professional skills to improve district decision‑making and transparency without adding cost.              |
| **Cash‑runway visibility**     | Show how forecasted spending erodes the General‑Fund balance and days‑cash‑on‑hand.                               |
| **Per‑pupil benchmarks**       | Compare Fredericktown’s \$/pupil spend and outcome metrics to peer districts using ODE data.                      |
| **Micro‑engagement model**     | Time‑boxed (≈10 hrs) pilot → evaluation → optional expansions.                                                    |
| **Open‑source stack**          | Streamlit + Pandas + GitHub Actions ▸ zero license fees, easy hand‑off.                                           |
| **GFOA & ODE alignment**       | Frame analyses with Smarter School Spending (GFOA) and Attendance Early‑Warning guidelines (ODE) for credibility. |

---

## 2. Objectives

1. **Increase budget transparency** for board members, staff, and taxpayers.
2. Provide **actionable insights** (cash runway, high‑growth cost lines, attendance risk) that inform policy and spending decisions.
3. Deliver a **public, auto‑updated dashboard** within one month, at no cost to the district.
4. Build trust that can lead to further analytics or IT modernization work.

---

## 3. Actions & Deliverables

### 3.1 Pre‑Work (completed / in‑progress)

| Action                                                             | Status | Deliverable                                    |
| ------------------------------------------------------------------ | ------ | ---------------------------------------------- |
| Extract key figures from Nov‑2024 Five‑Year Forecast               | ✅      | `Fredericktown_LSD_Key_Financials_FY24‑29.csv` |
| Load into notebook → DataFrame                                     | ✅      | Prototype DataFrame visible in chat            |
| Initial Streamlit dashboard (cash‑runway slider + per‑pupil chart) | ⏳      | Local prototype & PNG screenshot               |

### 3.2 Outreach Package

| Item                                          | Purpose                                                  |
| --------------------------------------------- | -------------------------------------------------------- |
| **Mock e‑mail** to Treasurer & Exec‑Secretary | Secures a 20‑min scoping call                            |
| PNG Screenshot                                | Demonstrates immediate value visually                    |
| Forecast CSV extract                          | Shows work is based solely on public data                |
| 1‑page MOU draft                              | Sets scope, data boundaries, 30‑day review, no liability |

### 3.3 Pilot Engagement (upon acceptance)

| Week | Task                                                 | Output                    |
| ---- | ---------------------------------------------------- | ------------------------- |
| 1    | Secure read‑only data access; finalize MOU           | Signed agreement          |
| 1‑2  | Deploy Streamlit app on Render/Netlify               | Public dashboard URL      |
| 2    | Quick‑win insight (e.g., spending‑velocity heat‑map) | Added dashboard view      |
| 3    | Internal review with Treasurer                       | Feedback & next‑step list |
| 4    | Optional board‑meeting demo                          | 2‑minute presentation     |

---

## 4. Decision Points & Reasoning

| Decision                            | Rationale                                                                               | Supporting Context                                           |
| ----------------------------------- | --------------------------------------------------------------------------------------- | ------------------------------------------------------------ |
| **Contact Treasurer first**         | Treasurer controls finance data and reports directly to board; can judge value quickly. | Small districts often lack a finance director layer.         |
| **CC Exec‑Secretary**               | Secretary routes external requests and manages Superintendent’s calendar.               | Ensures message is noticed even if Treasurer is busy.        |
| **Offer small, time‑boxed pilot**   | Reduces perceived risk and workload for district staff.                                 | Proven consulting tactic; easy “yes.”                        |
| **Use Streamlit + GitHub Actions**  | Fast to develop, no vendor lock‑in, no licensing.                                       | Aligns with open‑source ethos and district cost constraints. |
| **Anchor to GFOA & ODE frameworks** | Leverages recognized standards; bolsters credibility.                                   | Board members familiar with ODE compliance language.         |

---

## 5. Updated Checklist (live tracker)

| # | Task                                | Owner | Due    |
| - | ----------------------------------- | ----- | ------ |
| 1 | Polish Streamlit prototype & PNG    | Steve | Day 3  |
| 2 | Clean forecast CSV & docstring      | Steve | Day 3  |
| 3 | Draft 1‑page MOU                    | Steve | Day 4  |
| 4 | Send outreach e‑mail w/ attachments | Steve | Day 4  |
| 5 | Follow‑up if no response            | Steve | Day 11 |
| 6 | Prep board demo (if accepted)       | Steve | TBD    |

---

## 6. Reference Data & Tools

| Resource                           | Usage                                                   |
| ---------------------------------- | ------------------------------------------------------- |
| **Five‑Year Forecast (Nov 2024)**  | Source of revenue, expenditure, ending cash, days cash. |
| **ODE District Profile (FY 2023)** | Enrollment, valuation, staffing, spend per pupil.       |
| **GFOA Smarter School Spending**   | Framework for ROI and cost analyses.                    |
| **ODE Attendance EWS guidelines**  | Basis for potential attendance risk tile.               |
| **Streamlit & Pandas**             | Dashboard & data wrangling stack.                       |
| **GitHub Actions**                 | Nightly data refresh and static page build.             |

---

## 8. Purchased Services Analysis & Data‑Request Plan

### Why it matters

Line **3.030 – Purchased Services** shows the steepest growth in Fredericktown’s forecast, but the roll‑up hides which contracts or tuition bills are driving the increase.

### Data to request

| Priority | USAS extract needed                                                      | Insight gained                                                                                |
| -------- | ------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| 1        | **Object summary (400‑499), FY 21‑24 actual + FY 25 plan**               | Pinpoint which code bands (e.g., 460 Tuition vs. 420 Utilities) accelerate fastest.           |
| 2        | **Detailed ledger, FY 24 YTD, objects 460‑469**                          | Identify high‑cost tuition invoices (open enrollment, CCP, special‑ed placements).            |
| 3        | **Vendor history for utilities (electric, gas, water) – last 24 months** | Separate rate hikes from usage increases in 42X/47X costs.                                    |
| 4        | **Object‑by‑function matrix (400‑499 × function 1100/2500/2700)**        | Reveal whether inflation is instructional (special‑ed) or operational (facilities/transport). |

### Dashboard add‑on

* **“Purchased Services drill‑down” tab**

  * YoY growth % by object code (heat‑map, red > 5 %).
  * Top‑10 vendors/tuition destinations with trend lines.
  * CSV download for filtered ledger–ready for board review.

### Action timeline

| # | Task                                            | Owner | Due                   |
| - | ----------------------------------------------- | ----- | --------------------- |
| A | Request object summary & ledger from Treasurer  | Steve | Day 1 post‑acceptance |
| B | Build pivot chart & drill‑down tab in Streamlit | Steve | Day 3                 |
| C | Review insights with Treasurer                  | Steve | Day 4                 |
| D | Present findings to Board (if warranted)        | Steve | Next board mtg        |

---

## 7. Next Opportunities (Phase 2+ Ideas)

* **Transportation route optimizer** – GIS + bell‑time scenarios (potential \$250 K savings).
* **Utility‑bill anomaly detection** – monthly kWh vs. degree‑days.
* **Substitute‑cost dashboard** – link Aesop/Frontline to payroll for true absence cost.
* **Open data microsite** – CSV/JSON feeds for transparency & community trust.
