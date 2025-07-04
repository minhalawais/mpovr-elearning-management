import React, { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { ArrowRight, GraduationCap, Briefcase, Globe, Rocket, Code, Server, Database, Cloud } from 'lucide-react'
import Navbar from './navbar.tsx'
import { useNavigate } from 'react-router-dom'

const HeroSection = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const navigate = useNavigate()
  const handleCheckEligibilityClick = () => {
    navigate('/apply');
  };
  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const eligibilityCriteria = [
    {
      title: "Academic Excellence",
      description: "Consistent academic record from high school onwards",
      icon: GraduationCap
    },
    {
      title: "Professional Experience",
      description: "Minimum 2+ years",
      icon: Briefcase
    },
    {
      title: "Communication Skills",
      description: "Demonstrate strong English proficiency",
      icon: Globe
    },
    {
      title: "Ability",
      description: "Ability to complete an intensive 90-day practicum",
      icon: Code 
    }
  ]

  const floatingIcons = [Code, Server, Database, Cloud]

  return (
    <header className="relative overflow-hidden min-h-screen flex flex-col bg-[#eeebfe]">
      {/* Navigation */}
      <Navbar />

      {/* Main Content */}
      <div className="container mx-auto px-6 pt-32 pb-16 relative z-10">
        <div className="max-w-4xl mx-auto text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            {/* Smaller Rocket icon in circle */}
            <motion.div
              className="w-16 h-16 bg-[#8b5cf6] rounded-full flex items-center justify-center mx-auto mb-6"
              whileHover={{ scale: 1.1, rotate: 360 }}
              transition={{ duration: 0.8 }}
            >
              <Rocket className="w-8 h-8 text-white" />
            </motion.div>

            <h1 className="text-5xl md:text-6xl font-bold mb-2 text-gray-800">
              Relaunch Your Career
            </h1>
            
            {/* Updated subheading */}
            <h2 className="text-2xl md:text-3xl font-semibold mb-6 text-black Blanks-script">
              Your second chance starts now
            </h2>
            
            {/* Updated paragraph */}
            <p className="text-xl text-gray-600 mb-6 leading-relaxed max-w-2xl mx-auto">
              Missed earlier opportunities or feel you're capable of more? Seize this moment to transform your career.
            </p>

            <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-16">
              {/* Updated button text */}
              <motion.button
                className="px-8 py-4 text-[#8b5cf6] bg-[#ede9fe] rounded-full font-semibold hover:bg-[#8b5cf6] hover:text-white shadow-lg"
                whileHover={{ scale: 1.05 }}
                onClick={handleCheckEligibilityClick}
              >
                Know More
              </motion.button>
              <motion.button
                className="px-8 py-4 bg-[#8b5cf6] text-white rounded-full font-semibold flex items-center gap-2 hover:from-[#3756C0] hover:to-[#399fc6] shadow-lg shadow-[#399fc6]/20"
                whileHover={{ scale: 1.05 }}
                onClick={handleCheckEligibilityClick}
              >
                Begin Your Journey
                <ArrowRight className="w-5 h-5" />
              </motion.button>
            </div>
          </motion.div>

          {/* Updated Payment Info Section */}
          <motion.div
            className="mb-8 p-6 rounded-xl bg-white shadow-lg border border-gray-200 hover:border-[#399fc6]/30 transition-all duration-300"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            whileHover={{ scale: 1.02 }}
          >
            <h2 className="text-3xl font-bold text-transparent bg-clip-text bg-black mb-3">
              Reskill Now, Pay Later
            </h2>
            <p className="text-[#999999] font-semibold text-lg">
              U.S. applicants can pay only after landing a job.
            </p>
          </motion.div>

          {/* Eligibility Criteria with enhanced styling */}
          <motion.div
            className="bg-white rounded-xl p-8 shadow-2xl"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h2 className="relative mb-12">
              <span className="text-3xl font-bold bg-clip-text text-transparent bg-black font-bold">
                Ready to Reskill?
              </span>
              <span className="block text-lg text-gray-600 mt-2 font-medium">
                Key Qualifications
              </span>
              <div className="absolute -bottom-4 left-1/2 transform -translate-x-1/2 w-24 h-1 bg-gradient-to-r from-[#8b5cf6] to-[#8b5cf6] rounded-full"></div>
            </h2>            
            <div className="grid md:grid-cols-2 gap-6">
              {eligibilityCriteria.map((criterion, index) => (
                <motion.div
                  key={index}
                  className="flex items-start gap-4 text-left group"
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ duration: 0.4, delay: 0.4 + (index * 0.1) }}
                  whileHover={{ scale: 1.02 }}
                >
                  <div className="bg-gradient-to-br from-[#8b5cf6] to-[#8b5cf6] p-3 rounded-lg group-hover:shadow-lg group-hover:shadow-[#399fc6]/20 transition-all duration-300">
                    <criterion.icon className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-gray-800 font-semibold mb-1">{criterion.title}</h3>
                    <p className="text-gray-600 text-sm">{criterion.description}</p>
                  </div>
                </motion.div>
              ))}
            </div>
            <motion.div
              className="mt-8 p-4 rounded-lg bg-[#8b5cf6]/10 border border-[#8b5cf6]/20"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.6, delay: 0.8 }}
            >
              <p className="text-black font-semibold">
                Ready to take the first step? Sign up and complete your profile today!
              </p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </header>
  )
}

export default HeroSection

