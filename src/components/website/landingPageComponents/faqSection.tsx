'use client'

import React, { useState } from 'react'
import { ChevronDown, ChevronUp, HelpCircle, Search, ArrowRight } from 'lucide-react'

interface FAQItem {
  question: string
  answer: string
}

const faqData: FAQItem[] = [
  {
    question: "What makes the MPOVR ERP training program unique?",
    answer: "Our program offers a world-class, responsive web platform accessible from any device. You'll benefit from personalized dashboards, virtual classrooms, and interactive features. Plus, our unique approach includes anonymous usernames for privacy and admin-moderated communications to ensure a professional learning environment."
  },
  {
    question: "How long do I have to complete the ERP training program?",
    answer: "You have up to 18 months from the initial enrollment date to complete your training. This flexible timeline allows you to balance your learning with other commitments while ensuring you have ample time to master the material."
  },
  {
    question: "What kind of support can I expect during the training?",
    answer: "You'll receive comprehensive support throughout your journey. This includes access to ERP Trainers for guidance, a dedicated Admin team to facilitate communication, and a robust Learning Management System with study materials, quizzes, and assignments. We also offer career transformation support, including mock interviews and resume optimization."
  },
  {
    question: "How does the MPOVR platform ensure the security of my data?",
    answer: "We take security seriously. Our platform implements two-factor authentication (preferably via Microsoft Authenticator), role-based access control, and is hosted on AWS with 99.9% uptime. All communications are moderated, and we use system-generated usernames to protect your privacy."
  },
  {
    question: "Can I interact directly with trainers and other learners?",
    answer: "Yes, but with a unique twist for your protection. All communication between learners and trainers is routed through our Admin team for approval. This ensures a professional environment and prevents the exchange of personal contact details. You'll use an anonymous, system-generated username for all interactions."
  },
  {
    question: "What happens if I can't complete the program within 18 months?",
    answer: "If you don't complete the training within 18 months from the initial enrollment date, you'll need to re-enroll by paying the full training fee again. We encourage you to stay on track with your studies, and our support team is always here to help you manage your learning schedule effectively."
  },
  {
    question: "How does the MPOVR platform prepare me for real-world ERP challenges?",
    answer: "Our platform offers a mix of theoretical knowledge and practical application. You'll engage in virtual classrooms, work on real-world assignments, and participate in interactive sessions led by industry experts. The platform's analytics tools also provide real-time feedback on your progress, helping you identify and improve on areas that need attention."
  },
  {
    question: "What career support does MPOVR offer after program completion?",
    answer: "Upon successful completion of the program, you become eligible for our career support services. This includes assistance with resume optimization, mock interviews to hone your skills, and guidance on transitioning into ERP-related roles. Our goal is to not just train you, but to help transform your career trajectory."
  }
]

const FAQItem: React.FC<{ item: FAQItem; isOpen: boolean; toggleOpen: () => void }> = ({ item, isOpen, toggleOpen }) => (
  <div className="border-b border-[#8b5cf6]/20 last:border-b-0">
    <button
      className="flex justify-between items-center w-full py-4 px-4 text-left focus:outline-none transition-all duration-300 hover:bg-[#edf6f9]"
      onClick={toggleOpen}
    >
      <span className="font-semibold text-black pr-6 text-base">{item.question}</span>
      {isOpen ? (
        <ChevronUp className="w-5 h-5 text-[#8b5cf6] flex-shrink-0 transition-transform duration-300" />
      ) : (
        <ChevronDown className="w-5 h-5 text-[#8b5cf6] flex-shrink-0 transition-transform duration-300" />
      )}
    </button>
    {isOpen && (
      <div className="px-4 pb-4 text-gray-600 animate-fadeIn leading-relaxed text-sm">
        {item.answer}
      </div>
    )}
  </div>
)

const FAQSection: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  const filteredFAQs = faqData.filter(item =>
    item.question.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.answer.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <section className="py-12 bg-white relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-30"></div>
      <div className="container mx-auto px-6 relative z-10">
        <div className="text-center mb-8">
          <div className="inline-block p-2 rounded-full bg-[#8b5cf6]/10 mb-2">
            <HelpCircle className="w-8 h-8 text-[#8b5cf6]" />
          </div>
          <h2 className="text-3xl font-bold text-black mb-4">Frequently Asked Questions</h2>
          <p className="text-base text-gray-600 max-w-xl mx-auto leading-relaxed">
            Get answers to common questions about our ERP learning platform and how it can transform your career.
          </p>
        </div>
        <div className="max-w-3xl mx-auto mb-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Search FAQs..."
              className="w-full py-3 px-4 pr-10 rounded-full border border-[#8b5cf6] focus:outline-none focus:ring-2 focus:ring-[#8b5cf6] focus:border-transparent text-sm transition-all duration-300"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
            <Search className="absolute right-4 top-1/2 transform -translate-y-1/2 text-[#8b5cf6] w-5 h-5" />
          </div>
        </div>
        <div className="max-w-3xl mx-auto bg-white rounded-xl shadow-md overflow-hidden">
          {filteredFAQs.map((item, index) => (
            <FAQItem
              key={index}
              item={item}
              isOpen={index === openIndex}
              toggleOpen={() => setOpenIndex(index === openIndex ? null : index)}
            />
          ))}
        </div>
        {filteredFAQs.length === 0 && (
          <p className="text-center text-gray-600 mt-6 text-sm">No matching FAQs found. Please try a different search term or contact our support team for assistance.</p>
        )}

      </div>
    </section>
  )
}

export default FAQSection