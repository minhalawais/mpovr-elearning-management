'use client'

import React, { useState } from 'react'
import { ChevronDown, ChevronUp, HelpCircle } from 'lucide-react'

interface FAQItem {
  question: string
  answer: string
}

const faqData: FAQItem[] = [
  {
    question: "What are the eligibility criteria for the MPOVR program?",
    answer: "To be eligible for the MPOVR program, you need at least 2+ years of work experience, a strong academic record (consistent from high school to your final qualification), and good communication skills."
  },
  {
    question: "How long does the training program last?",
    answer: "The duration of the training program varies depending on the specific course you choose. However, you have up to 18 months from the initial enrollment date to complete your training."
  },
  {
    question: "What is the fee structure for the program?",
    answer: "There is a nominal registration fee to verify your eligibility. Once selected, you'll need to pay the full training fee, which includes certification costs. The exact amount can be discussed during the enrollment process."
  },
  {
    question: "Can I withdraw from the program after it begins?",
    answer: "After the program begins, withdrawal is not permitted. However, discontinuation is allowed for valid reasons such as medical emergencies or other circumstances outlined in the agreement."
  },
  {
    question: "What happens if I can't complete the program within 18 months?",
    answer: "If you don't complete the training within 18 months from the initial enrollment date, you'll need to pay the full training fee again to re-enroll."
  }
]

const FAQItem: React.FC<{ item: FAQItem; isOpen: boolean; toggleOpen: () => void }> = ({ item, isOpen, toggleOpen }) => (
  <div className="border-b border-[#83c5be]">
    <button
      className="flex justify-between items-center w-full py-5 px-4 text-left focus:outline-none"
      onClick={toggleOpen}
    >
      <span className="font-semibold text-[#006d77]">{item.question}</span>
      {isOpen ? (
        <ChevronUp className="w-5 h-5 text-[#006d77]" />
      ) : (
        <ChevronDown className="w-5 h-5 text-[#006d77]" />
      )}
    </button>
    {isOpen && (
      <div className="px-4 pb-5 text-gray-600 animate-fadeIn">
        {item.answer}
      </div>
    )}
  </div>
)

const FAQSection: React.FC = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null)

  return (
    <section className="py-20 bg-[#edf6f9]">
      <div className="container mx-auto px-4">
        <div className="text-center mb-12">
          <HelpCircle className="w-16 h-16 mx-auto mb-4 text-[#006d77]" />
          <h2 className="text-3xl font-bold text-[#006d77] mb-4">Frequently Asked Questions</h2>
          <p className="text-gray-600 max-w-2xl mx-auto">
            Find answers to common questions about our program, eligibility, and more.
          </p>
        </div>
        <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
          {faqData.map((item, index) => (
            <FAQItem
              key={index}
              item={item}
              isOpen={index === openIndex}
              toggleOpen={() => setOpenIndex(index === openIndex ? null : index)}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default FAQSection