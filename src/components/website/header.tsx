import React, { useEffect, useState } from 'react'
import { ArrowRight, Globe, Target, BookOpen, CheckCircle, ChevronDown, Code, Database, Server, Users, Zap, Shield } from 'lucide-react'
import { motion } from 'framer-motion'
import mpovrLogo from '../images/mpovr_logo.png'; // Adjust the path if necessary

const HeroSection: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const floatingIcons = [
    { icon: Code, top: '10%', left: '5%' },
    { icon: Database, top: '20%', right: '10%' },
    { icon: Server, bottom: '15%', left: '8%' },
    { icon: Users, bottom: '25%', right: '5%' },
    { icon: Zap, top: '40%', left: '15%' },
    { icon: Shield, top: '60%', right: '12%' },
  ]

  return (
    <header className="relative overflow-hidden min-h-screen flex flex-col bg-gradient-to-br from-[#399fc6] to-[#3756C0] font-roboto">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjZmZmIiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9yZWN0Pgo8L3N2Zz4=')] opacity-20" />
      <div className="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent" />

      {/* Floating Icons */}
      {floatingIcons.map((item, index) => (
        <motion.div
          key={index}
          className="absolute text-white/20 z-10"
          style={{ ...item, position: 'absolute' }}
          animate={{
            y: [0, 15, 0],
            rotate: [0, 5, -5, 0],
          }}
          transition={{
            duration: 6,
            repeat: Infinity,
            repeatType: 'reverse',
            delay: index * 0.5,
          }}
        >
          <item.icon size={48} />
        </motion.div>
      ))}

      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-white/90 backdrop-blur-md py-2 shadow-lg' : 'bg-transparent py-6'}`}>
        <div className="container mx-auto px-6 flex items-center justify-between">
          <motion.div 
            className="text-2xl font-bold flex items-center space-x-3 cursor-pointer font-benzin"
            whileHover={{ scale: 1.05 }}
            transition={{ type: "spring", stiffness: 400, damping: 10 }}
          >
          <div className="flex items-center">
            <img src={mpovrLogo} alt="Company Logo" className="h-16 w-16 mr-2 shadow-lg" />
            <span className={`MontserratFont text-2xl ${isScrolled ? 'text-[#3756C0]' : 'text-white'}`}>
              mpovr
            </span>
          </div>    
          </motion.div>
          <div className="space-x-8 hidden md:flex items-center">
            {['Programs', 'Learning Path', 'Dashboards', 'About'].map((item) => (
              <motion.button
                key={item}
                className={`transition-colors relative group text-sm font-medium ${isScrolled ? 'text-[#333333] hover:text-[#399fc6]' : 'text-white hover:text-[#edf6f9]'}`}
                whileHover={{ scale: 1.1 }}
                transition={{ type: "spring", stiffness: 400, damping: 10 }}
              >
                {item}
                <span className={`absolute bottom-0 left-0 w-0 h-0.5 ${isScrolled ? 'bg-[#399fc6]' : 'bg-white'} transition-all group-hover:w-full`}></span>
              </motion.button>
            ))}
            <motion.button 
              className={`px-6 py-2 rounded-full font-semibold transition-all shadow-lg hover:shadow-xl text-sm ${isScrolled ? 'bg-[#399fc6] text-white' : 'bg-white text-[#399fc6]'}`}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Apply Now
            </motion.button>
          </div>
        </div>
      </nav>

      <div className="container mx-auto px-6 py-24 pb-2 flex-grow flex items-center justify-center relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          <motion.div 
            className="inline-block px-4 py-2 bg-white/10 backdrop-blur-md rounded-full text-sm mb-6"
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            🚀 Transform Your Career with ERP Expertise
          </motion.div>
          <motion.h1 
            className="text-5xl md:text-7xl font-bold mb-8 leading-[1.1] text-white font-benzin"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
          >

            World-Class ERP
            <span className="bg-gradient-to-r from-[#edf6f9] to-[#E18400] bg-clip-text text-transparent block mt-2">
              Practicum Learning Programs
            </span>
          </motion.h1>
          <motion.p 
            className="text-xl mb-10 text-[#edf6f9] leading-relaxed max-w-2xl mx-auto"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
          >
            Elevate your professional journey through our comprehensive ERP training platform. 
            Engage in virtual classrooms, interactive modules, and gain hands-on experience with 
            cutting-edge enterprise technologies.
          </motion.p>
          <motion.div 
            className="space-x-6 mb-12"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
          >
            <motion.button 
              className="bg-[#E18400] text-white px-8 py-4 rounded-full font-semibold hover:bg-opacity-90 transition-all inline-flex items-center shadow-xl hover:shadow-2xl"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Start Your Journey <ArrowRight className="ml-2" />
            </motion.button>
            <motion.button 
              className="border-2 border-white px-8 py-4 rounded-full font-semibold hover:bg-white hover:text-[#3756C0] transition-all shadow-lg hover:shadow-xl text-white"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              Explore Programs
            </motion.button>
          </motion.div>

          {/* New Component: Testimonial Carousel */}
          <TestimonialCarousel />

        </div>
      </div>

      <div className="bg-[#edf6f9]/10 backdrop-blur-md py-16 mt-12">
        <div className="container mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            {[
              { 
                icon: Target, 
                title: "Comprehensive Learning Path", 
                description: "Navigate through structured modules, virtual classrooms, and interactive assignments designed to build real-world ERP expertise."
              },
              { 
                icon: BookOpen, 
                title: "Advanced Training Modules", 
                description: "Access prerecorded sessions, engage in live discussions, and complete assessments that prepare you for professional challenges." 
              },
              { 
                icon: CheckCircle, 
                title: "Career Support", 
                description: "Periodic grading, performance tracking, and career guidance to help you transition smoothly into enterprise technology roles." 
              }
            ].map((feature, index) => (
              <motion.div 
                key={index} 
                className="text-center group bg-[#edf6f9]/5 backdrop-blur-md rounded-xl p-6 hover:bg-[#edf6f9]/10 transition-all duration-300 border-2 border-transparent hover:border-[#E18400]"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.2 }}
                whileHover={{ 
                  scale: 1.05, 
                  transition: { duration: 0.2 } 
                }}
              >
                <motion.div 
                  className="relative inline-block mb-6"
                  whileHover={{ 
                    scale: 1.1,
                    rotate: 360,
                    transition: { duration: 0.3 }
                  }}
                >
                  <div className="absolute inset-0 bg-[#399fc6] rounded-full opacity-20 group-hover:opacity-30 group-hover:bg-[#E18400] transition-all duration-300 blur"></div>
                  <feature.icon className="w-16 h-16 text-[#edf6f9] group-hover:text-[#E18400] relative z-10 transition-colors duration-300" />
                </motion.div>
                <h3 className="text-2xl font-bold mb-4 text-[#edf6f9] group-hover:text-[#E18400] transition-colors duration-300 font-benzin">
                  {feature.title}
                </h3>
                <p className="text-[#edf6f9] group-hover:text-white transition-colors duration-300">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </div>

      <motion.div 
        className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        animate={{ y: [0, 10, 0] }}
        transition={{ repeat: Infinity, duration: 1.5 }}
      >
        <ChevronDown className="w-8 h-8 text-[#edf6f9] opacity-50 hover:opacity-100 transition-opacity duration-300 cursor-pointer" />
      </motion.div>
    </header>
  )
}

const TestimonialCarousel: React.FC = () => {
  const testimonials = [
    { name: "John Doe", role: "ERP Specialist", quote: "MPOVR Training transformed my career. The hands-on experience was invaluable." },
    { name: "Jane Smith", role: "IT Manager", quote: "The comprehensive curriculum and expert instructors set MPOVR apart from other training programs." },
    { name: "Alex Johnson", role: "Business Analyst", quote: "I gained practical skills that I use daily in my job. Highly recommended!" },
  ]

  return (
    <motion.div 
      className="bg-white/10 backdrop-blur-md rounded-xl p-6 mt-12"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.8 }}
    >
      <h2 className="text-2xl font-bold text-white mb-4">What Our Learners Say</h2>
      <div className="overflow-hidden">
        <motion.div 
          className="flex"
          animate={{ x: [0, -100 * testimonials.length + 100] }}
          transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
        >
          {testimonials.concat(testimonials).map((testimonial, index) => (
            <div key={index} className="w-full flex-shrink-0 px-4">
              <p className="text-[#edf6f9] italic mb-2">"{testimonial.quote}"</p>
              <p className="text-white font-semibold">{testimonial.name}</p>
              <p className="text-[#edf6f9] text-sm">{testimonial.role}</p>
            </div>
          ))}
        </motion.div>
      </div>
    </motion.div>
  )
}


export default HeroSection

