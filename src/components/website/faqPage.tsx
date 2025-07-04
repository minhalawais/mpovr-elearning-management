'use client'

import React, {useEffect} from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown } from 'lucide-react'
import Navbar from './landingPageComponents/navbar.tsx'

interface FAQItem {
  question: string;
  answer: string;
}

const faqs: FAQItem[] = [
  {
    question: "What is MPOVR?",
    answer: "MPOVR is a comprehensive IT training program designed to help individuals transform their careers and enter the high-growth IT industry. We offer intensive training in various IT fields, coupled with career support to launch your new tech career."
  },
  {
    question: "What programs does MPOVR offer?",
    answer: "MPOVR offers a range of programs including Full Stack Web Development, Data Science and Machine Learning, Cloud Computing and DevOps, Cybersecurity, Database Administration, and UI/UX Design. Each program is crafted to provide you with the skills and knowledge demanded by top employers in the tech industry."
  },
  {
    question: "What are the eligibility criteria for MPOVR programs?",
    answer: "The key eligibility criteria include a strong academic record from high school to final qualification, a minimum of 2+ years of professional experience, good communication skills, and an aspiration to enter high-growth global IT careers. However, each application is evaluated holistically, considering various factors beyond these basic requirements."
  },
  {
    question: "How long do the programs typically last?",
    answer: "Program durations vary depending on the specific course and individual progress. Typically, our programs range from 8 to 14 months. For example, the Full Stack Web Development program is 12 months, while the Database Administration program is 8 months."
  },
  {
    question: "Is there a fee for the program?",
    answer: "Yes, there is a fee for the program. However, we offer flexible payment options, including a special '$0 down' offer for US citizens where you only pay after you get hired. The full training fee, including certification costs, is disclosed during the application process."
  },
  {
    question: "What is the application process like?",
    answer: "The application process involves several steps: 1) Check eligibility, 2) Sign up and create a profile, 3) Pay a registration fee (waived for some applicants), 4) Schedule and attend an interview, 5) Complete the selection process, 6) Sign the training agreement, 7) Choose your start date, and 8) Begin your training journey."
  },
  {
    question: "Do you provide job placement assistance after completion of the program?",
    answer: "Yes, we provide ongoing career support to our graduates. This includes assistance with job placement in the IT industry. Our goal is to help you not just complete the program, but to launch your new career in tech."
  },
  {
    question: "What if I need to discontinue the program?",
    answer: "Once the program begins, withdrawal is generally not permitted except for valid reasons such as medical emergencies. In case of approved discontinuation, you can re-enroll in the same category within 18 months without additional fees. If training is not completed within 18 months from the initial enrollment date, the full training fee must be paid for re-enrollment."
  },
  {
    question: "How are the programs delivered?",
    answer: "Our programs are delivered through a combination of online learning platforms, live virtual classes, hands-on projects, and mentorship sessions. This blended approach ensures you get both theoretical knowledge and practical skills."
  },
  {
    question: "Are there any prerequisites for joining the programs?",
    answer: "While specific technical skills are not always required, a basic understanding of computer operations is beneficial. Each program may have its own set of recommended prerequisites, which will be communicated during the application process."
  }
]

const FAQItem: React.FC<{ item: FAQItem; isOpen: boolean; toggleOpen: () => void }> = ({ item, isOpen, toggleOpen }) => {
  return (
    <motion.div
      className="border-b border-gray-200 last:border-b-0"
      initial={false}
      animate={{ backgroundColor: isOpen ? "rgba(139, 92, 246, 0.1)" : "rgba(255, 255, 255, 0)" }}
      transition={{ duration: 0.3 }}
    >
      <button
        className="flex justify-between items-center w-full py-4 px-4 text-left focus:outline-none"
        onClick={toggleOpen}
      >
        <span className="text-lg font-medium text-gray-800">{item.question}</span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.3 }}
        >
          <ChevronDown className="w-5 h-5 text-[#8b5cf6]" />
        </motion.div>
      </button>
      <AnimatePresence initial={false}>
        {isOpen && (
          <motion.div
            initial="collapsed"
            animate="open"
            exit="collapsed"
            variants={{
              open: { opacity: 1, height: "auto" },
              collapsed: { opacity: 0, height: 0 }
            }}
            transition={{ duration: 0.3 }}
          >
            <div className="px-4 pb-4 text-gray-600">
              {item.answer}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  )
}

const FAQPage: React.FC = () => {
  const [openIndex, setOpenIndex] = React.useState<number | null>(null)
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="min-h-screen bg-gradient-to-b from-[#edf6f9] to-white relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-96 bg-gradient-to-b from-[#8b5cf6]/10 to-transparent"></div>
      <Navbar />
      
      <div className="container mx-auto px-4 py-24 relative z-10">
        <motion.h1 
          className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-800"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Frequently Asked <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#8b5cf6] to-[#6366f1] MontserratFont">Questions</span>
        </motion.h1>
        <motion.p 
          className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Find answers to common questions about MPOVR programs, eligibility, and the application process.
        </motion.p>

        <motion.div
          className="bg-white rounded-2xl shadow-lg border border-gray-200 max-w-3xl mx-auto overflow-hidden"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          {faqs.map((faq, index) => (
            <FAQItem
              key={index}
              item={faq}
              isOpen={openIndex === index}
              toggleOpen={() => setOpenIndex(openIndex === index ? null : index)}
            />
          ))}
        </motion.div>

        <motion.div
          className="mt-12 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <p className="text-gray-600 mb-4">Still have questions? We're here to help!</p>
          <a
            href="/contact"
            className="inline-block px-6 py-3 bg-[#8b5cf6] text-white rounded-lg font-semibold text-lg hover:bg-[#7c3aed] transition-all duration-300 shadow-lg shadow-[#8b5cf6]/30 flex items-center justify-center space-x-2 group"
          >
            <span>Contact Us</span>
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
            </svg>
          </a>
        </motion.div>
      </div>
    </div>
  )
}

export default FAQPage

