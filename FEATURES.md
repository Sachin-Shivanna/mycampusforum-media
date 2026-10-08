# MyCampusForum — Feature Catalog (source of truth for social posts)

All daily posting tasks (LinkedIn, Instagram, X/Twitter) pick features from this file. A weekly sync task adds new features from the app repo (Sachin-Shivanna/AlumniConnect).

**Rules for posts**
- `live` → describe as available. `testing` → only "coming soon" / "sneak peek" / building-in-public framing. `roadmap` → "coming soon" only.
- `NEW` flag → announce it once on each platform within ~7 days (LinkedIn: Tue spotlight or Wed building-in-public; Instagram: Tue Reel or Thu carousel; X: any day), then clear the flag once the LinkedIn and Instagram Last featured columns are filled.
- Never claim user counts, customer names or results. Screenshots only from `screenshots/` (redacted). If a feature has no screenshot, use a text/quote/poll/tips card — never mock up UI.
- **Variety:** in any 7 consecutive posts on a platform, at most 2 may centre on job matching/referrals/placements; at least 3 must centre on other features below. Prefer the feature with the oldest "Last featured" date for that platform.
- After posting, update the platform's "Last featured" cell for the feature(s) used (YYYY-MM-DD) and push.

| ID | Feature | Who it helps | What it does (plain words) | Status | Screenshot | Last featured LinkedIn | Last featured Instagram | Last featured X |
|---|---|---|---|---|---|---|---|---|
| F01 | AI job matching & explained matches | Alumni, students | Alumni post a role; AI reads the JD, ranks the top 5 best-fit students in minutes (up to 20), each with a plain-language "why this match" | live | job-ai-matches.png | 2026-10-12 | 2026-10-15 | |
| F02 | Company matches (auto job discovery) | Alumni, students | Open roles at alumni's companies are matched to students automatically so alumni can pass profiles along with one click | live | — | | | |
| F03 | Referrals & warm intros | Students, alumni | Student sees referral matches; recruiter–student chat opens; outcomes tracked (interview, offer) | live | connections-pipeline.png | 2026-10-14 | 2026-10-13 | |
| F04 | Real-time 1:1 chat with lifecycle | Students, alumni | Live recruiter–student chat; archived automatically when the role closes, so students aren't left hanging | live | — | | | |
| F05 | AI Community Channels | Alumni, students | AI spots natural groups (company, batch, department, role), creates channels, opt-in invites; auto-archives inactive ones | live | community-channel-chat.png | 2026-10-13 | 2026-10-15 | |
| F06 | Engagement bots (news, polls, Q&A) | Alumni, students | Industry news Mon/Wed, career polls Tue/Thu, discussion prompt Fri keep channels alive without staff effort | live | community-channel-chat.png | | | |
| F07 | Alumni-hosted sessions (AMAs, workshops, mock interviews) | Students, alumni | Alumni propose sessions, students register, join links + calendar built in | live | student-sessions-browse.png / alumni-host-sessions.png | 2026-10-10 | 2026-10-15 | |
| F08 | AI session-topic suggestions for alumni | Alumni | Monthly AI suggestions of what to teach, based on student interests | live | alumni-host-sessions.png | | | |
| F09 | Student session requests | Students | Students request the session topics they want; admins see them instantly | live | — | | | |
| F10 | Admin session review & re-approval | Institutions | Admins approve sessions before students register; edited sessions go back for re-approval, registered students are notified | live | admin-session-review.png | | | |
| F11 | Built-in video rooms (sessions & interviews) | Everyone | Gated video meetings with per-user join tokens and attendance for sessions and channel interviews | testing | — | | | |
| F12 | Course Materials marketplace | Faculty, students, institutions | Faculty create course folders and upload PDFs; students request access; watermarked viewer; ratings; cross-institution listing and purchase | live (NEW) | — | | | |
| F13 | Faculty role | Faculty, institutions | Faculty get their own profile and student view inside the institution space | live (NEW) | — | | | |
| F14 | PayForward (alumni giving) | Alumni, students, institutions | Alumni contribute to student aid funds with personal thank-yous; Razorpay/Stripe; admin tracking | testing | — (live screenshot shows amounts — do not use) | | | |
| F15 | Graduation flow (student → alumni) | Students, institutions | Graduating batches move from student to alumni accounts in one step with a public activation page | testing | — | | | |
| F16 | Student profile builder & resume upload | Students | Profile strength score, skills, LinkedIn/portfolio links, drag-and-drop resume that powers matching | live | student-dashboard.png | | | |
| F17 | Verified alumni (corporate email + admin approval) | Institutions, students | Alumni verified via corporate email and an admin approval queue, so students know who they're talking to | live | — | | | |
| F18 | Bulk invitations (CSV import) | Institutions | Invite thousands of students/alumni from a CSV with templates, de-duplication and history | live | — | | | |
| F19 | Announcements (email + in-app) | Institutions | Broadcast to students, alumni or specific channels with sent/read tracking | live | — | | | |
| F20 | Admin dashboard & placement funnel | Institutions | One view of students, alumni, connections, sessions, flags and the match → interview → offer funnel | live | admin-dashboard.png | | | |
| F21 | Student facilitation status | Institutions | See who never logged in, who's missing a resume, who's active — and nudge them | live | — | | | |
| F22 | Content moderation (flags) | Institutions | Flagged content goes to admins before it affects users; escalation workflow | live | — | | | |
| F23 | Support inbox / Contact Admin | Everyone | Students and alumni message the admin team directly; admins work a shared inbox | live | — | | | |
| F24 | Real-time notifications | Everyone | Approvals, announcements, registrations and cancellations update live in ~1 second, no refresh | live (NEW) | — | | | |
| F25 | Guided welcome tours | Everyone | Role-specific in-app tours for first-time students, alumni, faculty and admins | live (NEW) | — | | | |
| F26 | Mobile app (iOS & Android) | Everyone | Native app for students, alumni and admins: chat, channels, sessions, referrals, jobs, admin console, dark mode | testing — confirm store launch before saying "download" | — | | | |
| F27 | Private branded institution space | Institutions | Each institution gets its own subdomain and data isolated at the database level (row-level security) | live | — | | | |
| F28 | Dark mode & accent themes | Everyone | Light/dark themes and colour palettes across web and mobile | live | — | | | |
| R01 | LinkedIn profile auto-fill | Students | Paste a LinkedIn URL to pre-fill your profile | roadmap | — | | | |
| R02 | AI Channels for students | Students | Students join the same AI channels as alumni before graduation | roadmap | — | | | |

## Sync log
- 2026-10-08: added "Last featured X" column (X/Twitter channel connected; week-1 X drafts reuse LinkedIn cards for F05/F07/F01/F03).
- 2026-10-08: catalog created from README, TASK_STATUS_AND_QA.md, web/mobile source and git history up to 2026-10-07 (Course Materials changes 1–5, Faculty profile, Application Tour, realtime notifications).
