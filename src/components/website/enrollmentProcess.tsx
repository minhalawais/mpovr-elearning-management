'use client'

import React, {useEffect} from 'react'
import { motion } from 'framer-motion'
import { CheckCircle, Clock, DollarSign, GraduationCap, Briefcase, Globe, FileText, Calendar, Video, Award, Book, Users } from 'lucide-react'
import Navbar from './landingPageComponents/navbar.tsx'

const CriteriaPage = () => {
  const eligibilityCriteria = [
    { icon: GraduationCap, title: "Strong Academic Record", description: "Consistent performance from high school to final qualification" },
    { icon: Briefcase, title: "Work Experience", description: "Minimum 2+ years of professional experience" },
    { icon: Globe, title: "Communication Skills", description: "Excellent verbal and written communication abilities" },
  ]

  const journeySteps = [
    { 
      icon: CheckCircle, 
      title: "1. Check Eligibility", 
      description: "Ensure you meet our basic criteria to apply for the program." 
    },
    { 
      icon: FileText, 
      title: "2. Sign Up & Create Profile", 
      description: "Register on our platform and complete your basic profile with essential information." 
    },
    { 
      icon: DollarSign, 
      title: "3. Pay Registration Fee", 
      description: "Submit a nominal fee for us to verify your eligibility. For US citizens: $0 down payment option available!" 
    },
    { 
      icon: Calendar, 
      title: "4. Schedule Interview", 
      description: "Book a 15-minute slot with our enrollment administrator for a brief interview." 
    },
    { 
      icon: Video, 
      title: "5. Attend Interview", 
      description: "Showcase your skills, experience, and motivation during the interview." 
    },
    { 
      icon: Award, 
      title: "6. Selection Process", 
      description: "Our team will review your profile and interview. If selected, you'll receive an acceptance notification." 
    },
    { 
      icon: FileText, 
      title: "7. Complete Agreement", 
      description: "Sign the online training agreement and pay the full training fee (USD XXXX, including certification costs)." 
    },
    { 
      icon: Clock, 
      title: "8. Choose Start Date", 
      description: "Select your preferred program start date from the available options." 
    },
    { 
      icon: Book, 
      title: "9. Begin Your Journey", 
      description: "Start your intensive training program and transform your career!" 
    },
    { 
      icon: Users, 
      title: "10. Career Support", 
      description: "Upon successful completion, receive ongoing career support to launch your IT career." 
    },
  ]
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);
  return (
    <div className="min-h-screen bg-[#edf6f9] relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-96 bg-gradient-to-b from-[#8b5cf6]/10 to-transparent"></div>
      <Navbar />
      
      <div className="container mx-auto px-4 py-24 relative z-10">
        <motion.h1 
          className="text-4xl md:text-5xl font-bold text-center mb-4 text-gray-800"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          Your Path to an <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#8b5cf6] to-[#6366f1] MontserratFont">Exciting IT Career</span>
        </motion.h1>

        <motion.p 
          className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          We are dedicated to helping individuals transform their careers and enter the high-growth IT industry. Our comprehensive program is designed to equip you with the skills and knowledge needed to succeed in the global IT market.
        </motion.p>

        {/* Eligibility Criteria */}
        <motion.div 
          className="bg-white rounded-2xl p-8 mb-12 shadow-lg border border-gray-200"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Eligibility Criteria</h2>
          <div className="grid md:grid-cols-3 gap-8">
            {eligibilityCriteria.map((criterion, index) => (
              <motion.div 
                key={index} 
                className="flex flex-col items-center text-center group"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 0.6 + index * 0.1 }}
              >
                <div className="w-16 h-16 rounded-xl bg-[#8b5cf6]/10 flex items-center justify-center mb-4 group-hover:bg-[#8b5cf6]/20 transition-all duration-300">
                  <criterion.icon className="w-8 h-8 text-[#8b5cf6] group-hover:scale-110 transition-transform" />
                </div>
                <h3 className="text-xl font-semibold mb-2 text-gray-800 group-hover:text-[#8b5cf6] transition-colors">{criterion.title}</h3>
                <p className="text-gray-600">{criterion.description}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Journey Steps */}
        <motion.div 
          className="bg-white rounded-2xl p-8 mb-12 shadow-lg border border-gray-200"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.8 }}
        >
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Your Journey</h2>
          <div className="grid md:grid-cols-2 gap-8">
            {journeySteps.map((step, index) => (
              <motion.div 
                key={index} 
                className="flex items-start space-x-4 group"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: 1 + index * 0.1 }}
              >
                <div className="w-14 h-14 rounded-xl bg-[#8b5cf6]/10 flex items-center justify-center shrink-0 group-hover:bg-[#8b5cf6]/20 transition-all duration-300">
                  <step.icon className="w-7 h-7 text-[#8b5cf6] group-hover:scale-110 transition-transform" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold mb-2 text-gray-800 group-hover:text-[#8b5cf6] transition-colors">{step.title}</h3>
                  <p className="text-gray-600">{step.description}</p>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Special Offer */}
        <motion.div 
          className="bg-gradient-to-r from-[#8b5cf6]/20 to-[#6366f1]/20 rounded-2xl p-8 mb-12 border border-[#8b5cf6]/30"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 1.2 }}
        >
          <h2 className="text-3xl font-bold mb-4 text-center text-gray-800">Special Offer for US Citizens</h2>
          <p className="text-xl text-center text-gray-600 mb-6">
            Start your journey today with <span className="font-bold text-[#8b5cf6]">$0 down</span> and pay only after you get hired!
          </p>
          <div className="flex justify-center">
            <motion.button
              className="px-8 py-3 bg-[#8b5cf6] text-white rounded-lg font-semibold text-lg hover:bg-[#7c3aed] transition-all duration-300 shadow-lg shadow-[#8b5cf6]/30 flex items-center space-x-2 group"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <span>Start Your Application</span>
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
              </svg>
            </motion.button>
          </div>
        </motion.div>

        {/* Additional Information */}
        <motion.div 
          className="bg-white rounded-2xl p-8 shadow-lg border border-gray-200"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 1.4 }}
        >
          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">Important Information</h2>
          <div className="space-y-4 text-gray-600">
            {[
              "The full training fee, including certification costs, is USD XXXX.",
              "Program duration is typically 18 months, but may vary based on individual progress.",
              "After the program begins, withdrawal is not permitted except for valid reasons such as medical emergencies.",
              "In case of approved discontinuation, re-enrollment in the same category is possible within 18 months without additional fees.",
              "If training is not completed within 18 months from the initial enrollment date, full training fee must be paid for re-enrollment.",
              "Successful completion of the program includes periodic assessments and a final evaluation.",
              "Career support is provided to graduates to assist in job placement in the IT industry."
            ].map((info, index) => (
              <div key={index} className="flex items-start space-x-2">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-[#8b5cf6] mt-1 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <p>{info}</p>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  )
}

export default CriteriaPage