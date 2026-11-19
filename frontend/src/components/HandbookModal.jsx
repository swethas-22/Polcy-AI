import React from 'react';
import { X, BookOpen, Download, FileText, CheckCircle2 } from 'lucide-react';
import SKASCCrest from './SKASCCrest';

export default function HandbookModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  const policiesList = [
    "1. About the College, Governance and Applicability",
    "2. Admission Policy",
    "3. Academic Policy",
    "4. Attendance Policy (75% Minimum Requirement & Condonation)",
    "5. Examination and Evaluation Policy (10-point scale & Malpractice)",
    "6. Fee Structure, Payment and Refund Policy (UGC Refund Norms)",
    "7. Scholarship and Financial Assistance Policy (Govt & Merit Awards)",
    "8. Student Code of Conduct and Discipline Policy",
    "9. Anti-Ragging Policy (Zero-tolerance & UGC compliance)",
    "10. Prevention of Sexual Harassment and Gender Equity Policy (IC)",
    "11. Grievance Redressal and Equal Opportunity Policy",
    "12. Library Policy (Lending limits & digital resources)",
    "13. Information Technology and Acceptable Use Policy",
    "14. Data Privacy and Records Management Policy (DPDP Act)",
    "15. Campus Safety, Security and Health Policy",
    "16. Hostel Policy (Timings, mess, rules)",
    "17. Transport Policy (College bus routes & passes)",
    "18. Placement and Career Development Policy (TPC rules)",
    "19. Research, Publication Ethics and Anti-Plagiarism Policy (UGC tiers)",
    "20. Faculty and Staff Service Policy (Recruitment & workload)",
    "21. Leave Policy for Staff (CL, Medical, Maternity, Paternity, OD)",
    "22. Financial Management, Procurement and Audit Policy",
    "23. Infrastructure, Maintenance and Environmental Sustainability Policy",
    "24. Internal Quality Assurance, Accreditation and Compliance Policy (NAAC/NIRF)",
    "25. Policy Review, Amendment and Interpretation"
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4 backdrop-blur-2xs animate-in fade-in duration-150">
      <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] border border-[#E2DAD0] shadow-2xl p-6 text-xs sm:text-sm flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-[#F0EAE1]">
          <div className="flex items-center gap-3">
            <SKASCCrest size={40} />
            <div>
              <h3 className="text-base font-bold text-[#0F1E36]">SKASC Official Policy Handbook</h3>
              <p className="text-xs text-[#64748B]">Administrative Policies and Regulations • Edition 2026–2027</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg hover:bg-[#F2ECE1] text-[#64748B]">
            <X size={18} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto my-4 pr-2 space-y-3">
          <div className="p-3.5 rounded-xl bg-[#FAF6EE] border border-[#E9DFCE] text-xs text-[#554026]">
            <p className="font-semibold text-[#0F1E36] mb-1">Sri Krishna Arts and Science College, Coimbatore</p>
            <p className="leading-relaxed">
              This manual sets out the complete institutional policies covering academic regulations, 75% attendance criteria, continuous internal assessment, UGC fee refund tiers, anti-ragging measures, staff service rules, and environmental sustainability.
            </p>
          </div>

          <div>
            <h4 className="font-bold text-[#0F1E36] text-xs uppercase tracking-wider mb-2 text-[#83633C]">
              25 Official Policy Chapters (Indexed in Polcy AI):
            </h4>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
              {policiesList.map((p, i) => (
                <div key={i} className="flex items-start gap-2 p-2 rounded-lg bg-[#FCFBF9] border border-[#EDE5D8] text-[11.5px] text-[#334155]">
                  <CheckCircle2 size={13} className="text-[#9E7A4E] mt-0.5 flex-shrink-0" />
                  <span className="font-medium">{p}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <div className="pt-3 border-t border-[#F0EAE1] flex items-center justify-between">
          <span className="text-[11px] text-[#64748B]">
            Word Document Source: SKASC_Policy_Manual_2026_2027.docx
          </span>
          <button
            onClick={onClose}
            className="px-4 py-1.5 rounded-xl bg-[#12223D] text-white text-xs font-semibold hover:bg-[#1E355B]"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
