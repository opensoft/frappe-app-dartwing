# Dartwing Associations Module

**HOA, Country Clubs, Alumni Groups, Professional Societies & Every Membership Organization**  
2026–2027 Feature Set – Built on the unified `Organization` core (`org_type = Association`)

| Feature                                | HOA / Condo Association Example                                                          | Country Club / Yacht Club Example                                     | Alumni Association / Professional Society Example                  | Implementation Notes (Frappe + DartwingFone)                                                  |
| -------------------------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------------- |
| **Membership Tiers & Auto-Billing**    | Annual dues + special assessments (e.g., new roof) → automatic invoicing and late fees   | Platinum / Gold / Social / Junior tiers with different privileges     | Active Member / Lifetime / Student tiers                           | `Membership Tier` doctype → recurring invoices via Stripe / WeChat Pay / ACH                  |
| **Online Voting & Proxy Support**      | Board elections, bylaw amendments, budget approval → verifiable, auditable, mobile-first | Officer elections, capital project votes                              | Constitution changes, scholarship votes                            | `Voting Ballot` doctype with weighted voting, proxy assignment, QR-code voting from app       |
| **Violation & Fine Workflow**          | Unapproved fence → resident submits photo → committee reviews → fine → appeal path       | Dress-code or boat-dock violation (rare)                              | Code-of-conduct breach                                             | Mobile-first violation report → photo upload → automated escalation → payment link for fines  |
| **Facilities & Amenity Booking**       | Pool, tennis courts, clubhouse, guest suites                                             | Golf tee times, dining room, banquet hall, boat slips                 | Lecture halls, conference rooms for reunions                       | Real-time calendar integrated with DartwingFone → push reminders + cancelation penalties      |
| **Architectural Review (ARC)**         | Submit exterior changes → plans + photos → committee comments → approve/deny             | Rare (usually only new construction)                                  | N/A                                                                | Dedicated ARC request form → versioned PDF storage → digital signatures                       |
| **Reserve Fund & Budget Tracker**      | Required by law in most US states → 10-year reserve study + monthly contributions        | Capital reserve for clubhouse renovation                              | Endowment / scholarship fund tracking                              | `Reserve Study` doctype → visual health dashboard → automatic transfer suggestions            |
| **Owner / Member Portal & Mobile App** | Pay dues, submit maintenance tickets, view meeting minutes, download tax docs            | Book tee times, view statements, RSVP to events, see member directory | Register for reunion, update contact info, donate, read newsletter | Same DartwingFone app → context automatically switches to Association when opened in that org |
| **Document Vault & Meeting Minutes**   | Covenants, bylaws, meeting minutes, insurance certificates                               | Club bylaws, event photos, historical tournament results              | Chapter charter, past conference proceedings                       | Encrypted file storage → version history → one-tap sharing                                    |
| **Emergency Broadcast System**         | Hurricane → instant push + SMS to every unit                                             | Lightning closure → immediate tee-time cancellation                   | Urgent dues deadline or event change                               | One-tap “Send to All Members” from mobile or desktop → supports SMS fallback                  |
| **Gate / Guest Access Management**     | Pre-approve guests → temporary QR code → guard scans on entry                            | Guest passes for non-members                                          | Guest passes for reunions                                          | QR code generated in app → scanned by guard tablet or resident phone                          |
| **Delinquency & Collections Workflow** | 30-/60-/90-day reminders → lien → foreclosure path (state-specific)                      | Suspension of privileges after 60 days                                | Removal from directory after X years                               | Automated dunning → payment plans → integration with local attorneys (future)                 |
| **Board & Committee Management**       | President, Treasurer, ARC Chair → term tracking, task assignments                        | Commodore, House Committee, Membership Committee                      | Chapter President, Treasurer, Events Chair                         | Role Template system auto-creates board roles → term expiration alerts                        |
| **Event Management & RSVP**            | Annual meeting, pool parties, holiday events                                             | Member-Guest tournament, wine dinner, junior clinic                   | Homecoming, regional meetups, gala                                 | Built-in event creator → RSVP → push reminders → check-in QR codes                            |
| **Directory with Privacy Controls**    | Opt-in/opt-out of phone/email visibility                                                 | Same + handicap index visibility                                      | Opt-in professional title & employer                               | Granular privacy settings per member → still allows emergency reach                           |

### Bonus HOA-Specific Power Features (2027+)

- **Insurance Certificate Tracker** – auto-remind owners to upload current policy
- **Work Order & Vendor Management** – landscaping, pool service, elevator maintenance
- **Capital Improvement Voting** – multi-million-dollar projects with quorum + 67 % approval
- **State-Law Compliance Packs** – pre-loaded rules for Florida, California, Texas, Nevada, etc.

All of the above lives in the **Dartwing Associations** module — activated the moment an `Organization` is created with `org_type = Association`.  
Same DartwingFone mobile app. Same AI engine. Same global `Person` records. Zero data silos.

This module alone replaces every legacy HOA software (AppFolio Community, Buildium, TOPS, Vantaca, etc.) and every country-club system (Jonas, Clubessential, Northstar) — at 1/5th the price and with a 10× better mobile experience.

Ready to ship Q1 2027 — right after Company and Family modules are GA.

Want the full Frappe doctype list for Dartwing Associations (`Membership Tier`, `Voting Ballot`, `HOA Violation`, `Reserve Study`, etc.) next?
