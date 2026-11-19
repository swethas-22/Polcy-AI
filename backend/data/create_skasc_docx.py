import os
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_policy_document(filepath):
    doc = Document()
    
    # Title & Header
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_t1 = title_p.add_run("SRI KRISHNA ARTS AND SCIENCE COLLEGE\n")
    run_t1.bold = True
    run_t1.font.size = Pt(20)
    run_t1.font.color.rgb = RGBColor(15, 30, 54) # Deep Navy
    
    run_t2 = title_p.add_run("Coimbatore, Tamil Nadu, India\n")
    run_t2.font.size = Pt(13)
    run_t2.font.color.rgb = RGBColor(100, 100, 100)
    
    run_t3 = title_p.add_run("ADMINISTRATIVE POLICIES AND REGULATIONS\n")
    run_t3.bold = True
    run_t3.font.size = Pt(16)
    run_t3.font.color.rgb = RGBColor(180, 120, 30) # Golden brown
    
    run_t4 = title_p.add_run("Policy Manual for Students, Faculty and Staff\n")
    run_t4.font.size = Pt(12)
    run_t4.italic = True
    
    run_t5 = title_p.add_run("Edition: 2026–2027 | Issued: 19 November 2026\n")
    run_t5.font.size = Pt(10)
    run_t5.font.color.rgb = RGBColor(120, 120, 120)

    doc.add_paragraph("Note: Sri Krishna Arts and Science College is a model institution. This manual sets out the administrative framework and common practices followed by established arts and science colleges in India.")
    
    doc.add_heading("Contents", level=1)
    contents = [
        "1. About the College, Governance and Applicability",
        "2. Admission Policy",
        "3. Academic Policy",
        "4. Attendance Policy",
        "5. Examination and Evaluation Policy",
        "6. Fee Structure, Payment and Refund Policy",
        "7. Scholarship and Financial Assistance Policy",
        "8. Student Code of Conduct and Discipline Policy",
        "9. Anti-Ragging Policy",
        "10. Prevention of Sexual Harassment and Gender Equity Policy",
        "11. Grievance Redressal and Equal Opportunity Policy",
        "12. Library Policy",
        "13. Information Technology and Acceptable Use Policy",
        "14. Data Privacy and Records Management Policy",
        "15. Campus Safety, Security and Health Policy",
        "16. Hostel Policy",
        "17. Transport Policy",
        "18. Placement and Career Development Policy",
        "19. Research, Publication Ethics and Anti-Plagiarism Policy",
        "20. Faculty and Staff Service Policy",
        "21. Leave Policy for Staff",
        "22. Financial Management, Procurement and Audit Policy",
        "23. Infrastructure, Maintenance and Environmental Sustainability Policy",
        "24. Internal Quality Assurance, Accreditation and Compliance Policy",
        "25. Policy Review, Amendment and Interpretation"
    ]
    for c in contents:
        doc.add_paragraph(c, style='List Bullet')
        
    doc.add_heading("Preface", level=1)
    doc.add_paragraph(
        "This Policy Manual sets out the administrative framework of Sri Krishna Arts and Science College. "
        "It is meant to give students, parents, faculty and staff a clear and consistent understanding of the rights, "
        "responsibilities and procedures that apply in the College. The policies have been prepared with reference to "
        "the regulations of the University Grants Commission, the Government of India and the Government of Tamil Nadu, "
        "and the practices commonly followed by well-established arts and science colleges in India.\n"
        "Dates, amounts, timings and limits stated in this manual are indicative and may be adjusted by the Governing "
        "Council in accordance with the changes in applicable regulations. Every member of the College community is "
        "expected to read and follow these policies.\n\nPrincipal\nSri Krishna Arts and Science College"
    )

    # Section 1
    doc.add_heading("1. About the College, Governance and Applicability", level=1)
    doc.add_paragraph("1.1 Sri Krishna Arts and Science College (hereafter \"the College\") is a co-educational institution offering undergraduate, postgraduate and research programmes in the arts, sciences, commerce and management streams. The College functions under the management of the Sri Krishna Educational Trust (hereafter \"the Management\") and is affiliated to its affiliating University (hereafter \"the University\").")
    doc.add_paragraph("1.2 Vision: To be a centre of excellence that develops knowledgeable, skilled, ethical and socially responsible citizens through quality higher education.")
    doc.add_paragraph("1.3 Mission: (a) to provide accessible, learner-centred education of high quality; (b) to promote research, innovation and entrepreneurship; (c) to nurture values of integrity, inclusiveness and service to society.")
    doc.add_paragraph("1.4 These policies apply to all students, faculty, non-teaching staff, contract staff, research scholars, visitors and service providers on the campus or engaged in any College-organised activity, on or off campus.")
    doc.add_paragraph("1.5 The College follows the regulations, circulars and guidelines of the University Grants Commission (UGC), the Government of India, the Government of Tamil Nadu, the Department of Higher Education, the affiliating University and the statutory bodies concerned. Where these policies conflict with a statutory regulation, the regulation prevails.")
    doc.add_paragraph("1.6 Governing Council: The Governing Council, chaired by the Chairman of the Trust, is the apex decision-making body. It includes the Secretary, the Principal, a University nominee, a Government nominee where applicable, senior faculty representatives, an alumni representative and an academic expert.")
    doc.add_paragraph("1.7 Principal: The Principal is the academic and administrative head of the College and is responsible for implementing these policies, subject to the direction of the Governing Council.")
    
    t1 = doc.add_table(rows=1, cols=2)
    t1.style = 'Table Grid'
    hdr_cells = t1.rows[0].cells
    hdr_cells[0].text = "Body / Office"
    hdr_cells[1].text = "Principal Role"
    for cell in hdr_cells:
        set_cell_background(cell, "EAE5D9")
    
    roles = [
        ("Governing Council", "Policy approval, budget sanction, appointment of Principal, strategic planning"),
        ("Principal", "Overall administration, academic leadership, compliance with University and UGC norms"),
        ("Academic Council", "Curriculum implementation, academic calendar, examination matters, new programmes"),
        ("Heads of Departments (HoDs)", "Departmental teaching, timetables, internal assessment, faculty workload"),
        ("Controller of Examinations", "Conduct of internal and university examinations, results, revaluation"),
        ("Internal Quality Assurance Cell (IQAC)", "Quality benchmarks, NAAC/NIRF documentation, academic and administrative audit"),
        ("Administrative Officer / Office Superintendent", "Records, fee collection, staff administration, stores and maintenance")
    ]
    for b, r in roles:
        row = t1.add_row().cells
        row[0].text = b
        row[1].text = r

    # Section 2
    doc.add_heading("2. Admission Policy", level=1)
    doc.add_paragraph("2.1 Admissions are made strictly on merit and in accordance with the rules of the University, the Government of Tamil Nadu and the UGC, including the applicable reservation policy for Scheduled Castes, Scheduled Tribes, Backward Classes, Most Backward Classes, Differently-abled persons, Ex-servicemen wards, Sports persons and other notified categories.")
    doc.add_paragraph("2.2 Eligibility: An applicant must have passed the Higher Secondary (Class XII) examination or an equivalent examination recognised by the University, with the minimum marks prescribed for the programme. Postgraduate applicants must hold a relevant bachelor's degree from a recognised University.")
    doc.add_paragraph("2.3 Application and selection: Applications are accepted through the College admission portal or the prescribed form during the notified period. A rank list is prepared on the basis of qualifying marks (and any entrance test or interview prescribed for the programme) and is published on the College notice board and website.")
    doc.add_paragraph("2.4 Documents required at the time of admission:\n- Transfer Certificate and Conduct Certificate from the institution last attended\n- Mark sheets of the qualifying examination (originals for verification and attested copies)\n- Community Certificate and other eligibility certificates, as applicable\n- Migration Certificate (for students from other Boards or Universities)\n- Aadhaar card or other proof of identity and address\n- Passport-size photographs and a valid mobile number and email address")
    doc.add_paragraph("2.5 Admissions are provisional until verification of all original documents and payment of the prescribed fees. The College may cancel the admission of any student who has furnished false or forged information or documents, with no refund of fees, and may initiate further action as permitted by law.")
    doc.add_paragraph("2.6 Lateral entry, transfer from other colleges and re-admission are permitted only as allowed by the University regulations and subject to availability of seats.")
    doc.add_paragraph("2.7 Admission of international students and Non-Resident Indians is governed by the rules of the University and the Government of India. Foreign students must submit valid passport, visa and equivalence certificates.")
    doc.add_paragraph("2.8 The College does not charge any capitation fee or donation for admission. Receipts are issued for every payment, and fee amounts are published in the prospectus.")
    doc.add_paragraph("2.9 Admission Committee: The Principal constitutes an Admission Committee each year, including the Vice-Principal, HoDs and the Administrative Officer, to supervise admissions and resolve eligibility matters.")

    # Section 3
    doc.add_heading("3. Academic Policy", level=1)
    doc.add_paragraph("3.1 The academic year is divided into two semesters, odd (June to November) and even (December to April), under the Choice Based Credit System (CBCS) prescribed by the University. The academic calendar, including working days, examination periods and holidays, is published before the start of every academic year.")
    doc.add_paragraph("3.2 Programmes consist of core courses, elective courses, ability-enhancement and skill-enhancement courses, value-added courses and extension activities, as per the University syllabus. The minimum credits required for the award of a degree are those prescribed by the University.")
    doc.add_paragraph("3.3 Teaching is delivered through lectures, tutorials, practical sessions, seminars, assignments, projects, internships and field visits. Faculty must prepare a course plan and teaching diary for each course and submit them to the HoD.")
    doc.add_paragraph("3.4 Each department prepares a timetable that is approved by the Principal. A minimum of 90 working days per semester must be ensured as per UGC guidelines. Cancelled classes must be made up through additional or compensatory classes.")
    doc.add_paragraph("3.5 Mentoring: Each student is assigned a faculty mentor who monitors attendance, academic progress and well-being, and maintains the mentoring record.")
    doc.add_paragraph("3.6 Add-on and value-added courses, skill certification programmes, bridge courses and remedial coaching are offered to improve learning outcomes and employability.")
    doc.add_paragraph("3.7 Programme outcomes, programme-specific outcomes and course outcomes are communicated to students at the start of each course and are periodically reviewed by the IQAC.")
    doc.add_paragraph("3.8 Student feedback on teaching and the curriculum is collected at least once every semester. The analysis is reviewed by the Principal and shared with the concerned faculty and HoD.")
    doc.add_paragraph("3.9 Switching of programmes or elective courses is permitted only within the time stipulated by the University and with the approval of the Principal.")

    # Section 4
    doc.add_heading("4. Attendance Policy", level=1)
    doc.add_paragraph("4.1 A student must have a minimum of 75% attendance in each semester, across all courses, to be eligible to appear for the University semester examinations.")
    doc.add_paragraph("4.2 Attendance is recorded for every class period by the faculty concerned and is entered in the attendance register or the College management system. Attendance details are displayed at regular intervals and informed to parents or guardians where appropriate.")
    
    t4 = doc.add_table(rows=1, cols=2)
    t4.style = 'Table Grid'
    h4 = t4.rows[0].cells
    h4[0].text = "Attendance"
    h4[1].text = "Consequence"
    for c in h4:
        set_cell_background(c, "EAE5D9")
    att_rows = [
        ("75% and above", "Eligible for the semester examinations"),
        ("65% to below 75%", "May be considered for condonation on genuine grounds (such as medical reasons supported by a certificate) with the Principal's approval, subject to the University's rules and payment of the prescribed condonation fee"),
        ("Below 65%", "Not eligible for the semester examinations; the student must repeat the semester or course as per University rules")
    ]
    for a, c in att_rows:
        r = t4.add_row().cells
        r[0].text = a
        r[1].text = c

    doc.add_paragraph("4.3 Students representing the College or University in sports, NCC, NSS, cultural events or other authorised activities may be granted attendance for the duration of the event on submission of the prescribed approval, subject to the limits fixed by the University.")
    doc.add_paragraph("4.4 Leave must be applied for in writing, in advance wherever possible, through the mentor and the HoD. Absence for more than seven consecutive days without permission may result in the name being struck off the rolls after due notice.")
    doc.add_paragraph("4.5 Late arrival beyond 10 minutes may be marked as absence for that period at the discretion of the faculty member.")

    # Section 5
    doc.add_heading("5. Examination and Evaluation Policy", level=1)
    doc.add_paragraph("5.1 Continuous Internal Assessment (CIA): Internal marks are awarded on the basis of internal tests, assignments, seminars, attendance and other components, as prescribed by the University. At least two internal tests are conducted every semester.")
    doc.add_paragraph("5.2 Internal assessment marks are displayed to students, who may raise queries with the course teacher within five working days of publication. Final internal marks are submitted to the University within the prescribed deadline.")
    doc.add_paragraph("5.3 The Controller of Examinations coordinates all University examinations at the College centre in accordance with the University's instructions, including seating plans, invigilation, custody of question papers and answer scripts, and dispatch of answer scripts.")
    doc.add_paragraph("5.4 Students must carry their College identity card and hall ticket to the examination hall. Mobile phones, smart watches, calculators (unless permitted), written material and any unauthorised electronic devices are prohibited in the examination hall.")
    doc.add_paragraph("5.5 Examination malpractice, including copying, impersonation, passing of material, tampering with records and misbehaviour towards the invigilators, is dealt with as per the University's regulations. The College may additionally impose disciplinary action under the Code of Conduct.")
    doc.add_paragraph("5.6 Grading: The College follows the University's grading system. In the absence of a different University scheme, the following 10-point scale is applied.")
    
    t5 = doc.add_table(rows=1, cols=4)
    t5.style = 'Table Grid'
    h5 = t5.rows[0].cells
    h5[0].text = "Marks (%)"
    h5[1].text = "Grade"
    h5[2].text = "Grade Point"
    h5[3].text = "Remark"
    for c in h5:
        set_cell_background(c, "EAE5D9")
    grades = [
        ("90 – 100", "O", "10", "Outstanding"),
        ("80 – 89", "A+", "9", "Excellent"),
        ("70 – 79", "A", "8", "Very Good"),
        ("60 – 69", "B+", "7", "Good"),
        ("50 – 59", "B", "6", "Above Average"),
        ("40 – 49", "C", "5", "Pass"),
        ("Below 40", "F", "0", "Fail / Reappear")
    ]
    for m, g, gp, rm in grades:
        r = t5.add_row().cells
        r[0].text = m
        r[1].text = g
        r[2].text = gp
        r[3].text = rm

    doc.add_paragraph("5.7 Revaluation, re-totalling and retrieval of answer scripts are available as per the University's procedure and fee. The College facilitates the application process.")
    doc.add_paragraph("5.8 Results are communicated to students through the College notice board, portal and the University website. Mark statements and degree certificates are issued by the University and collected from the College office on the notified dates.")
    doc.add_paragraph("5.9 Arrear (re-appearance) examinations are permitted within the maximum duration allowed for the programme under the University regulations.")

    # Section 6
    doc.add_heading("6. Fee Structure, Payment and Refund Policy", level=1)
    doc.add_paragraph("6.1 The fees for each programme (tuition, special fee, laboratory fee, library fee, examination fee, development fee and others, as applicable) are approved by the Management in accordance with Government and University norms and are published in the prospectus. The fee schedule is displayed on the notice board.")
    doc.add_paragraph("6.2 Fees must be paid by the due dates notified by the office, through the online payment gateway, demand draft or at the College cash counter. Every payment is acknowledged by an official receipt.")
    doc.add_paragraph("6.3 Late payment: A late fee may be levied after the due date, as notified. Students with outstanding dues may be denied hall tickets, certificates, hostel and transport services, until the dues are cleared.")
    doc.add_paragraph("6.4 Fee instalments may be granted by the Principal in cases of genuine hardship on a written request supported by documents.")
    doc.add_paragraph("6.5 Refund of fees: The College follows the UGC fee refund norms. The following schedule applies to students who withdraw their admission.")
    
    t6 = doc.add_table(rows=1, cols=2)
    t6.style = 'Table Grid'
    h6 = t6.rows[0].cells
    h6[0].text = "Date of Withdrawal"
    h6[1].text = "Refund of Fees Paid"
    for c in h6:
        set_cell_background(c, "EAE5D9")
    ref_rows = [
        ("15 days or more before the formal commencement of the programme", "100% (less a processing fee of not more than ₹1,000)"),
        ("Less than 15 days before commencement", "90%"),
        ("Up to 15 days after commencement", "80%"),
        ("15 to 30 days after commencement", "50%"),
        ("More than 30 days after commencement", "No refund")
    ]
    for dw, rf in ref_rows:
        r = t6.add_row().cells
        r[0].text = dw
        r[1].text = rf

    doc.add_paragraph("6.6 Caution deposit (where collected) is refunded at the end of the course on submission of the no-dues certificate and the original receipt. Refunds are made by bank transfer within 30 working days after approval.")
    doc.add_paragraph("6.7 Fees once paid for a semester or year are not refundable on account of disciplinary dismissal, long absence or voluntary discontinuation after the cut-off date.")
    doc.add_paragraph("6.8 Original certificates deposited at admission are returned only after clearance of all dues and a no-dues certificate from the concerned departments, Library, Hostel and Office.")

    # Section 7
    doc.add_heading("7. Scholarship and Financial Assistance Policy", level=1)
    doc.add_paragraph("7.1 The College facilitates the application for Government scholarships and fee concessions, including those for SC/ST/BC/MBC students, minority students, differently-abled students, first-generation graduates and the Government-notified schemes such as the Pudhumai Penn and other applicable schemes, subject to the current guidelines.")
    doc.add_paragraph("7.2 The Scholarship Cell, headed by a faculty coordinator, informs students of eligibility and deadlines, helps with online applications and verifies documents.")
    doc.add_paragraph("7.3 Merit scholarship: Students who secure the top ranks in the University examinations or the College examinations may receive a merit award or partial fee concession, as sanctioned by the Management each year.")
    doc.add_paragraph("7.4 Management-funded financial aid: Deserving students with demonstrated financial need may be granted a fee concession by the Scholarship Committee, based on income proof, academic performance and conduct.")
    doc.add_paragraph("7.5 Sports and cultural concessions may be granted to students who have represented the College at the University, State or National level, as decided by the Management.")
    doc.add_paragraph("7.6 Scholarship and concession benefits may be withdrawn if the student's attendance, performance or conduct falls below the prescribed standards, or if false information has been submitted.")

    # Section 8
    doc.add_heading("8. Student Code of Conduct and Discipline Policy", level=1)
    doc.add_paragraph("8.1 Every student shall maintain discipline, respect the faculty and staff, and uphold the dignity of the College at all times, on and off campus.")
    doc.add_paragraph("8.2 Students must wear the College identity card on campus and carry it at all times. Students must follow the dress code of the College, which requires decent and appropriate attire. Uniform requirements, where prescribed, must be followed.")
    doc.add_paragraph("8.3 The following acts are prohibited and constitute misconduct:\n- Ragging, bullying, harassment or discrimination of any kind\n- Possession or use of alcohol, tobacco products, narcotic drugs or other prohibited substances on campus\n- Damage to College property, defacing of walls, or misuse of facilities and equipment\n- Use of mobile phones in classrooms, laboratories, the library and examination halls, except where permitted for academic purposes\n- Cheating, plagiarism, forgery or tampering with records\n- Possession of weapons or any dangerous materials\n- Participating in or organising unauthorised meetings, protests, strikes or political activities on campus\n- Misuse of social media to defame or harass the College, staff or fellow students")
    doc.add_paragraph("8.4 Disciplinary Committee: The Principal constitutes a Disciplinary Committee, including the Vice-Principal, senior faculty and the concerned HoD, to examine complaints of misconduct. The student concerned shall be given a notice and a fair opportunity to be heard.")
    doc.add_paragraph("8.5 Penalties, depending on the gravity of the offence, may include a verbal or written warning, a fine, parental intimation, suspension of classes, restriction of facilities, withholding of certificates, suspension for a specified period, or expulsion from the College. Serious offences may be reported to the police.")
    doc.add_paragraph("8.6 Student clubs, associations and elections: The College may allow formation of student bodies such as the Students' Union, NSS, NCC, YRC, Literary Club, Sports Club and others under the supervision of the Principal and faculty coordinators. Activities require prior permission.")
    doc.add_paragraph("8.7 Parents or guardians may be called to the College in cases of repeated absence, poor academic performance or misconduct.")

    # Section 9
    doc.add_heading("9. Anti-Ragging Policy", level=1)
    doc.add_paragraph("9.1 The College has a zero-tolerance policy on ragging in line with the UGC Regulations on Curbing the Menace of Ragging in Higher Educational Institutions, 2009, and the orders of the Supreme Court of India. Ragging in any form is a criminal offence.")
    doc.add_paragraph("9.2 Ragging includes any conduct, verbal, written, physical or by electronic means, that causes or is likely to cause annoyance, hardship, physical or psychological harm, or that compels a student to do something they would not do in the ordinary course.")
    doc.add_paragraph("9.3 Every student and the parent or guardian must submit an undertaking (affidavit) against ragging at the time of admission, as required by UGC. The undertaking can also be submitted online at the national anti-ragging portal.")
    doc.add_paragraph("9.4 Anti-Ragging Committee and Squad: The College constitutes an Anti-Ragging Committee chaired by the Principal, and an Anti-Ragging Squad, as per the UGC regulations. The Squad conducts surprise visits to classrooms, hostels, canteen, library, bus stops and other vulnerable places.")
    doc.add_paragraph("9.5 Complaints may be made to the Anti-Ragging Committee, the Principal, or the National Anti-Ragging Helpline (toll-free) 1800-180-5522 or helpline@antiragging.in. Complaint boxes are placed at prominent locations. The identity of the complainant is kept confidential.")
    doc.add_paragraph("9.6 Penalties include suspension from classes, withholding of scholarships, suspension or rustication, debarring from the examinations, expulsion, cancellation of admission, and a police complaint (FIR), without prejudice to any action under law.")
    doc.add_paragraph("9.7 Anti-ragging notices, contact numbers and the penalties are displayed prominently throughout the campus and in the prospectus and handbook.")

    # Section 10
    doc.add_heading("10. Prevention of Sexual Harassment and Gender Equity Policy", level=1)
    doc.add_paragraph("10.1 The College is committed to providing a safe, respectful and gender-sensitive environment for all students and employees, in accordance with the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013 and the UGC (Prevention, Prohibition and Redressal of Sexual Harassment of Women Employees and Students in Higher Educational Institutions) Regulations, 2015.")
    doc.add_paragraph("10.2 Internal Committee (IC): The Principal constitutes an Internal Committee chaired by a senior woman faculty member, with at least half of its members being women, a non-teaching staff member, student representatives, and an external member from an NGO or a person familiar with issues of sexual harassment.")
    doc.add_paragraph("10.3 Sexual harassment includes unwelcome physical contact, requests for sexual favours, sexually coloured remarks, showing pornography, and any other unwelcome physical, verbal or non-verbal conduct of a sexual nature, including through electronic means.")
    doc.add_paragraph("10.4 A complaint may be made in writing to the IC within three months of the incident (extendable by a further three months for sufficient reasons). The IC conducts an inquiry following the principles of natural justice and submits its report within 90 days.")
    doc.add_paragraph("10.5 The IC may recommend interim relief, including change of class or section, leave, or restraining orders. Penalties may include a warning, suspension, expulsion or termination of service, as per the College service rules and the applicable law.")
    doc.add_paragraph("10.6 The identity of the complainant, the respondent and witnesses is kept confidential. Retaliation against a complainant or a witness is strictly prohibited and is a separate offence.")
    doc.add_paragraph("10.7 The College conducts annual awareness and gender-sensitisation programmes. The name and contact numbers of IC members are displayed on the notice board and the website.")

    # Section 11
    doc.add_heading("11. Grievance Redressal and Equal Opportunity Policy", level=1)
    doc.add_paragraph("11.1 The College has a Grievance Redressal Committee in accordance with the UGC (Redress of Grievances of Students) Regulations, 2023, to address complaints relating to admission, fees, scholarships, examinations, discrimination, harassment, facilities and any other matter.")
    doc.add_paragraph("11.2 A grievance may be submitted in writing, by email or through the suggestion box. The Committee acknowledges the grievance within three working days and aims to resolve it within 15 working days. Where the matter is complex, the complainant is informed of the status.")
    doc.add_paragraph("11.3 If the student is not satisfied with the decision, the student may appeal to the Principal and, thereafter, to the Management or the University Ombudsperson, as applicable.")
    doc.add_paragraph("11.4 Equal Opportunity Cell: The College provides equal opportunities and does not discriminate on the grounds of caste, religion, gender, language, region, disability, economic status or any other ground. An SC/ST Cell, a Minority Cell and an Equal Opportunity Cell monitor the implementation of reservation and welfare measures.")
    doc.add_paragraph("11.5 Persons with disabilities: The College follows the Rights of Persons with Disabilities Act, 2016. Ramps, accessible washrooms, extra time or scribes in examinations and other reasonable accommodations are provided on request, supported by a valid certificate.")
    doc.add_paragraph("11.6 Students may also use the Suggestion and Feedback system. Anonymous complaints may be considered at the Principal's discretion where there is prima facie evidence.")

    # Section 12
    doc.add_heading("12. Library Policy", level=1)
    doc.add_paragraph("12.1 The Library is a central academic resource that provides textbooks, reference books, periodicals, journals, e-resources, e-books, previous question papers and project reports. Working hours are notified at the beginning of each semester.")
    doc.add_paragraph("12.2 Membership: All students and staff are members of the Library. A valid College identity card is required for entry and for borrowing books.")
    doc.add_paragraph("12.3 Lending limits (subject to change by the Librarian with the Principal's approval):")
    
    t12 = doc.add_table(rows=1, cols=3)
    t12.style = 'Table Grid'
    h12 = t12.rows[0].cells
    h12[0].text = "Member"
    h12[1].text = "Books Allowed"
    h12[2].text = "Loan Period"
    for c in h12:
        set_cell_background(c, "EAE5D9")
    lib_rows = [
        ("Undergraduate students", "2", "14 days"),
        ("Postgraduate students and research scholars", "3", "21 days"),
        ("Teaching staff", "5", "30 days"),
        ("Non-teaching staff", "2", "14 days")
    ]
    for m, b, lp in lib_rows:
        r = t12.add_row().cells
        r[0].text = m
        r[1].text = b
        r[2].text = lp

    doc.add_paragraph("12.4 Overdue books attract a fine as notified by the Library. Lost or damaged books must be replaced with the same or a latest edition or paid for at the current price, along with a processing fee.")
    doc.add_paragraph("12.5 Reference books, periodicals, rare books and project reports are for use within the Library only.")
    doc.add_paragraph("12.6 Silence and discipline must be maintained. Bags, food and beverages are not allowed in the reading area. Mobile phones must be kept on silent mode.")
    doc.add_paragraph("12.7 E-resources and digital library access (including NDL, e-journals and databases subscribed by the College) may be used only for educational and research purposes. Illegal downloading, sharing of credentials or bulk downloading is prohibited.")
    doc.add_paragraph("12.8 A Library Advisory Committee, including faculty and student representatives, meets at least once a year to review book acquisition, services and budget. An annual stock verification is carried out.")

    # Section 13
    doc.add_heading("13. Information Technology and Acceptable Use Policy", level=1)
    doc.add_paragraph("13.1 This policy governs the use of the College's computers, laboratories, network, internet, Wi-Fi, e-mail, learning management system, website and software by students, faculty and staff.")
    doc.add_paragraph("13.2 College IT resources must be used for academic, research and administrative purposes only. Personal use must be reasonable and must not interfere with academic or official work.")
    doc.add_paragraph("13.3 Users must keep their login credentials confidential and are responsible for all activity under their accounts. Sharing of passwords and unauthorised access to systems, accounts or data are prohibited.")
    doc.add_paragraph("13.4 The following are strictly prohibited: installing or distributing pirated software; accessing, storing or circulating obscene, hateful, defamatory or unlawful material; hacking, spreading malware or attempting to bypass security controls; cyberbullying; and using the network for commercial or political activities.")
    doc.add_paragraph("13.5 The IT Cell monitors the network for security and performance and may block websites or suspend accounts where there is a violation. Logs may be maintained and examined as permitted by law.")
    doc.add_paragraph("13.6 The College follows the Information Technology Act, 2000 and the applicable cyber laws. Violations are subject to disciplinary action and, where required, legal action.")
    doc.add_paragraph("13.7 Computer laboratories must be used under supervision. Food and drinks are not allowed. Any damage or malfunction must be reported to the lab in-charge immediately.")
    doc.add_paragraph("13.8 Regular backup of administrative data, anti-virus updates and a record of the equipment stock are maintained by the IT Cell. Obsolete equipment is disposed of as per the e-waste rules.")

    # Section 14
    doc.add_heading("14. Data Privacy and Records Management Policy", level=1)
    doc.add_paragraph("14.1 The College collects personal information about students, parents, staff and alumni only for legitimate academic, administrative and statutory purposes, and handles it in accordance with the Digital Personal Data Protection Act, 2023 and other applicable laws.")
    doc.add_paragraph("14.2 Access to student and staff records is limited to authorised persons. Personal data is shared with third parties (such as the University, Government agencies and scholarship bodies) only where required by law or with the consent of the individual.")
    doc.add_paragraph("14.3 Photographs and videos of College events may be used for publicity and the College website and social media. Students or parents who do not wish to be featured must inform the Office in writing.")
    doc.add_paragraph("14.4 Student academic records, fee records, admission files and service records are maintained in physical and electronic form. Records are retained for the periods prescribed by the University, the Government and audit requirements, and are thereafter disposed of securely.")
    doc.add_paragraph("14.5 Requests for certificates, transcripts, bonafide letters, conduct certificates and duplicate documents must be made to the Office on the prescribed form with the fee, if any. They are normally issued within seven working days.")
    doc.add_paragraph("14.6 Data breaches or loss of records must be reported immediately to the Principal and the IT Cell.")

    # Section 15
    doc.add_heading("15. Campus Safety, Security and Health Policy", level=1)
    doc.add_paragraph("15.1 The College provides a safe and secure campus. The campus is protected by security staff, controlled entry points, and, where installed, CCTV surveillance. Visitors must register at the main gate and obtain a visitor pass.")
    doc.add_paragraph("15.2 Students must carry the identity card while on campus. Parents and guests may meet students only at designated times and places and with the permission of the office.")
    doc.add_paragraph("15.3 Fire safety: Fire extinguishers and exits are provided as required, and fire safety drills are conducted at least once a year. Staff and students must cooperate during drills and emergencies.")
    doc.add_paragraph("15.4 A first-aid facility is maintained on campus, and the College has tie-ups with nearby hospitals for emergencies. Students with medical conditions are advised to inform the mentor or the office so that proper help can be provided.")
    doc.add_paragraph("15.5 Health and wellness: The College offers a Student Counselling Centre staffed by trained counsellors. Counselling is confidential and available for academic, personal and mental health concerns. Awareness sessions, health camps and blood donation drives are organised periodically.")
    doc.add_paragraph("15.6 Laboratory safety: Students and staff must follow safety rules, wear protective equipment and handle chemicals, biological materials and equipment in accordance with the safety instructions of the laboratory. Accidents must be reported immediately.")
    doc.add_paragraph("15.7 Smoking, alcohol, tobacco and drugs: The campus is a tobacco-free, alcohol-free and drug-free zone in line with the Cigarettes and Other Tobacco Products Act (COTPA), 2003 and the Narcotic Drugs and Psychotropic Substances Act. An Anti-Drug Committee organises awareness programmes and takes action on violations.")
    doc.add_paragraph("15.8 Emergency and disaster management: An Emergency Response Team prepares and reviews an emergency plan covering fire, natural calamities, medical emergencies and security threats, and displays the emergency contact numbers on the campus.")
    doc.add_paragraph("15.9 Vehicles: Two-wheeler riders must wear helmets and carry valid driving licences. Vehicles must be parked in designated areas and driven at slow speeds on campus. Parking is at the owner's risk.")

    # Section 16
    doc.add_heading("16. Hostel Policy", level=1)
    doc.add_paragraph("16.1 Separate hostels for men and women are provided on or near the campus, and admission is granted on a first-come, first-served basis, subject to availability and the prescribed hostel admission procedure. Priority may be given to students from distant places.")
    doc.add_paragraph("16.2 Hostel fees (rent, mess charges, electricity and other charges) and a refundable caution deposit are payable as notified. Mess charges may be revised depending on the cost of provisions.")
    doc.add_paragraph("16.3 Each hostel is managed by a Warden, assisted by Deputy Wardens and staff. The Hostel Committee, including student representatives, monitors food quality, hygiene and facilities.")
    doc.add_paragraph("16.4 Timings: Students must be inside the hostel by the time notified (generally 6:30 PM for women and 8:00 PM for men). Study hours are observed in the evening. Late entry requires prior written permission.")
    doc.add_paragraph("16.5 Leave and outings: Students may leave the hostel only after signing the movement register. Overnight leave requires the prior written permission of the parent or guardian and the Warden. Visitors are permitted only in the visitors' room at the permitted times.")
    doc.add_paragraph("16.6 Prohibited in the hostel: alcohol, tobacco, drugs, ragging, gambling, heavy electrical appliances (heaters, induction stoves), unauthorised guests, damage to furniture and fittings.")
    doc.add_paragraph("16.7 Residents are responsible for their belongings and the cleanliness of their rooms. Room inspections may be carried out by the Warden for safety and discipline.")
    doc.add_paragraph("16.8 Violations may result in a fine, warning, suspension or cancellation of the hostel seat, and also disciplinary action by the College.")

    # Section 17
    doc.add_heading("17. Transport Policy", level=1)
    doc.add_paragraph("17.1 The College operates buses on notified routes for students and staff. Routes, timings and stops are published at the beginning of each academic year.")
    doc.add_paragraph("17.2 Bus passes are issued on the payment of the annual or semester transport fee and must be carried at all times. Fees are non-refundable except in cases of cancellation before the start of the academic term.")
    doc.add_paragraph("17.3 Students must observe discipline, remain seated, not obstruct the doors and be punctual at the bus stops. The bus will not wait beyond the scheduled time.")
    doc.add_paragraph("17.4 Transport Committee: The Transport In-charge monitors the roadworthiness of vehicles, driver licences, insurance and fitness certificates, and ensures compliance with the motor vehicle rules. Drivers and conductors undergo periodic safety and conduct training.")
    doc.add_paragraph("17.5 Misbehaviour in vehicles may lead to the suspension of the bus pass and other disciplinary action.")

    # Section 18
    doc.add_heading("18. Placement and Career Development Policy", level=1)
    doc.add_paragraph("18.1 The Training and Placement Cell (TPC) organises campus recruitment drives, pre-placement training, internships, aptitude and soft skills training, mock interviews and career guidance for final-year students.")
    doc.add_paragraph("18.2 Eligibility: Students must have the minimum attendance and have no current arrears, as defined by the TPC, and must be registered with the Cell. Companies' own eligibility criteria also apply.")
    doc.add_paragraph("18.3 Students must conduct themselves professionally, attend all placement activities for which they register, and provide accurate information to the recruiters. Any student who misbehaves or who withdraws without proper reason after confirmation may be debarred from further placement activities.")
    doc.add_paragraph("18.4 Placement offers received through the College must be communicated to the TPC. A student who accepts an offer may be restricted from appearing for other drives, as per the TPC's rules for that academic year.")
    doc.add_paragraph("18.5 The College facilitates entrepreneurship development through the Entrepreneurship Development Cell and internships with industry partners. The Alumni Association supports mentoring and placement activities.")
    doc.add_paragraph("18.6 The TPC maintains placement records and reports the statistics to the IQAC and for NAAC and NIRF data submission.")

    # Section 19
    doc.add_heading("19. Research, Publication Ethics and Anti-Plagiarism Policy", level=1)
    doc.add_paragraph("19.1 The College encourages faculty and students to undertake research and publish in credible journals. A Research Advisory Committee guides the development of research proposals and the use of internal and external funding.")
    doc.add_paragraph("19.2 Plagiarism of any kind in assignments, projects, dissertations, theses and publications is prohibited. The College follows the UGC (Promotion of Academic Integrity and Prevention of Plagiarism in Higher Educational Institutions) Regulations, 2018.")
    doc.add_paragraph("19.3 All dissertations, theses and project reports must be checked with an approved plagiarism-detection tool before submission. The following similarity levels are applied as per the UGC regulations:")
    
    t19 = doc.add_table(rows=1, cols=2)
    t19.style = 'Table Grid'
    h19 = t19.rows[0].cells
    h19[0].text = "Similarity Level"
    h19[1].text = "Action"
    for c in h19:
        set_cell_background(c, "EAE5D9")
    plag_rows = [
        ("Up to 10%", "Minor similarity; no penalty"),
        ("10% to 40%", "Student must revise and resubmit the work within a period of not more than six months"),
        ("40% to 60%", "Debarred from submitting a revised version for up to one year"),
        ("Above 60%", "Registration or programme is cancelled for that work")
    ]
    for sl, act in plag_rows:
        r = t19.add_row().cells
        r[0].text = sl
        r[1].text = act

    doc.add_paragraph("19.4 Authorship, research data integrity, avoidance of fabrication and falsification, acknowledgement of sources and disclosure of conflicts of interest must be followed. Publications in predatory journals are discouraged, and the UGC-CARE list is used as a reference.")
    doc.add_paragraph("19.5 Research involving human or animal participants requires approval from the relevant ethics committee. Intellectual property created with College resources is governed by the IPR guidelines of the College.")
    doc.add_paragraph("19.6 Complaints of research misconduct are examined by an Academic Integrity Panel, which submits a report to the Principal.")

    # Section 20
    doc.add_heading("20. Faculty and Staff Service Policy", level=1)
    doc.add_paragraph("20.1 Recruitment: Teaching staff are appointed in accordance with UGC regulations, University norms and the Government of Tamil Nadu rules, and based on the qualification, experience and a selection process consisting of a screening, teaching demonstration and interview before a Selection Committee including a University nominee where applicable. Non-teaching staff are recruited through a transparent process, as per the educational qualifications and the experience set for each post.")
    doc.add_paragraph("20.2 Equal opportunity and reservation norms are followed in recruitment where applicable. Appointment orders specify the terms and conditions, including the probation period (generally one year, extendable).")
    doc.add_paragraph("20.3 Working hours: Working hours are notified by the Principal. Teaching staff must also take part in examination duty, evaluation, mentoring, committee work, admission, NAAC and other institutional work.")
    doc.add_paragraph("20.4 Workload: The teaching workload is allotted as per UGC norms, with typically 16 hours per week for Assistant Professors and 14 hours for Associate Professors and Professors, along with the research and administrative responsibilities.")
    doc.add_paragraph("20.5 Performance appraisal: Faculty submit an annual self-appraisal in the format prescribed, which is reviewed by the HoD and Principal. Student feedback, research output and contribution to the institution are considered. Appraisal is used for career advancement and awards.")
    doc.add_paragraph("20.6 Career advancement: Promotions under the Career Advancement Scheme follow UGC norms, and the staff are encouraged to attend orientation programmes, refresher courses, FDPs, workshops and conferences. Duty leave and financial support for these programmes are provided subject to approval.")
    doc.add_paragraph("20.7 Code of professional ethics: Staff must maintain high ethical and professional standards, avoid private tuition of the College's own students for gain, refrain from discrimination and harassment, and observe confidentiality of examination matters and student information.")
    doc.add_paragraph("20.8 Resignation and termination: A staff member who wishes to resign must give notice (generally one to three months, as stated in the appointment order). Services may be terminated for misconduct after a due enquiry, or for unsatisfactory performance after a warning and an opportunity for improvement.")
    doc.add_paragraph("20.9 Retirement age and retirement benefits are as per the Government and UGC rules for aided and unaided colleges. Staff welfare measures include provident fund, ESI (where applicable), gratuity, and a staff welfare fund.")

    # Section 21
    doc.add_heading("21. Leave Policy for Staff", level=1)
    t21 = doc.add_table(rows=1, cols=3)
    t21.style = 'Table Grid'
    h21 = t21.rows[0].cells
    h21[0].text = "Type of Leave"
    h21[1].text = "Entitlement (per year)"
    h21[2].text = "Remarks"
    for c in h21:
        set_cell_background(c, "EAE5D9")
    leave_rows = [
        ("Casual Leave (CL)", "12 days", "Cannot be combined with other leave beyond 3 days at a time without approval"),
        ("Earned / Vacation Leave", "As per Government and University norms", "Teaching staff are entitled to vacation as per the academic calendar"),
        ("Medical Leave", "Up to 10 days (with a medical certificate)", "Extended leave subject to approval"),
        ("Maternity Leave", "26 weeks (as per Maternity Benefit Act, as amended)", "Applicable for eligible women employees"),
        ("Paternity Leave", "Up to 15 days", "At the time of childbirth of a spouse, as per the approved rules"),
        ("Duty Leave / On Duty (OD)", "As sanctioned", "For FDPs, conferences, examination duty, University work and approved activities"),
        ("Loss of Pay Leave", "As approved", "Any leave beyond the entitlement")
    ]
    for tl, ent, rem in leave_rows:
        r = t21.add_row().cells
        r[0].text = tl
        r[1].text = ent
        r[2].text = rem

    doc.add_paragraph("21.1 Leave must be applied for in the prescribed form in advance and must be sanctioned by the HoD and the Principal. In emergencies, the staff member must inform the HoD or the office at the earliest. Unauthorised absence is treated as loss of pay and may attract disciplinary action.")
    doc.add_paragraph("21.2 Teaching staff taking leave must arrange for their classes to be handled by a colleague and must inform the HoD to avoid disruptions to the timetable.")
    doc.add_paragraph("21.3 Leave entitlements stated above are indicative and are subject to the rules of the Government, the University, and the terms of the appointment.")

    # Section 22
    doc.add_heading("22. Financial Management, Procurement and Audit Policy", level=1)
    doc.add_paragraph("22.1 The College budget is prepared annually by the Principal and the Administrative Officer and approved by the Governing Council. All income and expenditure are managed in accordance with the budget and the delegation of financial powers.")
    doc.add_paragraph("22.2 All collections are deposited in the College bank accounts, and the receipts are accounted for. Cash handling is minimised, and online payment is encouraged. Cash must be deposited within one working day.")
    doc.add_paragraph("22.3 Purchases above the limit fixed by the Governing Council require at least three quotations and approval by a Purchase Committee. Purchases are verified for quality and quantity by a Stock Verification Committee before payment. Conflict of interest must be declared.")
    doc.add_paragraph("22.4 Accounts are maintained as per the applicable accounting standards, and are audited every year by a qualified Chartered Accountant. Internal audit is carried out periodically. Government grants, if any, are utilised only for the purposes sanctioned, and Utilisation Certificates are submitted on time.")
    doc.add_paragraph("22.5 A stock register of all assets is maintained, and physical verification is conducted every year. Damaged or obsolete items are written off with the approval of the competent authority.")
    doc.add_paragraph("22.6 Financial information (fee structure, financial statements) is made available as required by law and as part of accreditation.")

    # Section 23
    doc.add_heading("23. Infrastructure, Maintenance and Environmental Sustainability Policy", level=1)
    doc.add_paragraph("23.1 The College provides adequate classrooms, laboratories, seminar halls, an auditorium, playgrounds, sports facilities, staff rooms, washrooms and drinking water facilities. A Maintenance Committee ensures that these are kept clean and in good condition.")
    doc.add_paragraph("23.2 Maintenance requests may be raised by students and staff through the Office or the complaints register. Routine repairs are completed within a reasonable period, and urgent repairs are attended to immediately.")
    doc.add_paragraph("23.3 Green campus: The College promotes a clean, green, and plastic-free campus. Initiatives include tree plantation, waste segregation, composting, rainwater harvesting, energy-efficient lighting, the use of solar energy where possible, and water conservation.")
    doc.add_paragraph("23.4 Waste management: Solid waste is segregated at source, and e-waste and hazardous waste are disposed of through authorised agencies as per the rules. Single-use plastics are discouraged.")
    doc.add_paragraph("23.5 An Eco Club and the NSS volunteers conduct environment awareness programmes. An environmental audit, a green audit and an energy audit are conducted periodically by the IQAC.")
    doc.add_paragraph("23.6 The use of College facilities (auditorium, grounds, halls) by outside agencies is permitted only with prior written approval from the Principal and on the payment of the prescribed charges.")

    # Section 24
    doc.add_heading("24. Internal Quality Assurance, Accreditation and Compliance Policy", level=1)
    doc.add_paragraph("24.1 The IQAC, headed by the Principal and coordinated by a senior faculty member, develops and monitors quality benchmarks and ensures continuous improvement of academic and administrative processes, in line with the guidelines of the NAAC and NIRF.")
    doc.add_paragraph("24.2 The IQAC prepares the Annual Quality Assurance Report (AQAR), conducts academic and administrative audits, analyses feedback from students, parents, alumni, employers and teachers, and recommends corrective measures.")
    doc.add_paragraph("24.3 Each department prepares an annual report and a plan of action. The College maintains documentation of teaching, research, extension activities and student support to meet the criteria for accreditation.")
    doc.add_paragraph("24.4 The College submits data on time to AISHE, NIRF, the University and the Government, and complies with the statutory requirements, such as the UGC mandatory disclosures on its website.")
    doc.add_paragraph("24.5 Extension and outreach: The College runs NSS, NCC, YRC and extension programmes, and adopts villages or communities for social service. Students are encouraged to participate and may earn extension credits as per the University norms.")
    doc.add_paragraph("24.6 The College conducts an annual day, sports day, and other activities that promote the all-round development of students. Participation in these events is encouraged and recognised.")

    # Section 25
    doc.add_heading("25. Policy Review, Amendment and Interpretation", level=1)
    doc.add_paragraph("25.1 These policies come into effect from the date of approval by the Governing Council and remain in force until amended or withdrawn.")
    doc.add_paragraph("25.2 The policies are reviewed at least once every two years, or earlier in the event of any change in the law, University or UGC regulations, or institutional needs. The IQAC coordinates the review process and recommends amendments to the Governing Council.")
    doc.add_paragraph("25.3 The Principal has the authority to issue circulars and guidelines to implement the policies and to decide on any matters not covered, in the interest of the College, subject to ratification by the Governing Council.")
    doc.add_paragraph("25.4 In case of any dispute on the interpretation of these policies, the decision of the Principal, and in the case of an appeal, the Governing Council, will be final, subject to applicable law.")
    doc.add_paragraph("25.5 Students and staff are expected to know and follow these policies. A copy is made available in the Library, the Office, and on the College website.")
    doc.add_paragraph("25.6 Any disputes shall be subject to the jurisdiction of the courts at Coimbatore, Tamil Nadu.")

    doc.save(filepath)
    print(f"Successfully generated {filepath}")

if __name__ == "__main__":
    out_path = os.path.join(r"d:\Polcy chatbot\backend\data", "SKASC_Policy_Manual_2026_2027.docx")
    create_policy_document(out_path)
