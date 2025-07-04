import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Menu, X } from 'lucide-react'
import mpovrLogo from '../../../images/mpovr_logo.png'

const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const navigate = useNavigate()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleClick = (item: string) => {
    if (item === 'How it Works') {
      navigate('/criteria')
    } else if (item === 'Programs') {
      navigate('/programs')
    } else if (item === 'Check Eligibility') {
      navigate('/apply')
    } else if (item === 'FAQ') {
      navigate('/faq')
    } else if (item === 'Contact Us') {
      navigate('/contact')
    }else if(item === 'Training Schedule'){
      navigate('/trainingschedule')
    }
    setIsMobileMenuOpen(false)
  }

  const handleSignUpClick = () => {
    navigate('/apply')
    setIsMobileMenuOpen(false)
  }

  const navItems = [
    'Programs', 
    'How it Works',
    'Training Schedule', 
    'FAQ', 
  ]

  return (
    <nav className={`
      fixed top-0 left-0 right-0 z-50 transition-all duration-300 
      ${isScrolled ? 'bg-white shadow-lg' : 'bg-white'}
    `}>
      <div className="container mx-auto px-6 py-4 flex items-center justify-between">
        {/* Logo */}
        <motion.div 
          className="text-2xl font-bold flex items-center space-x-3 cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onClick={() => navigate('/')}
        >         
          <img src={mpovrLogo} alt="MPOVR Logo" className="w-12 h-10" />
          <span className="text-transparent font-bold text-3xl bg-clip-text bg-[#8B5CF6] Benzin-font ml-0" style={{ marginLeft: '3px', marginTop: '12px' }}>mpovr</span>
        </motion.div>
      
        {/* Desktop Navigation */}
        <div className="space-x-6 hidden md:flex items-center">
          {navItems.map((item) => (
            <motion.button
              key={item}
              className="text-gray-800 text-sm font-medium hover:text-[#399fc6]"
              whileHover={{ scale: 1.1 }}
              onClick={() => handleClick(item)}
            >
              {item}
            </motion.button>
          ))}
          <motion.button 
            className="px-6 py-2 rounded-xl bg-[#8b5cf6] text-white font-semibold text-sm hover:bg-[#8b5cf6]"
            whileHover={{ scale: 1.05 }}
            onClick={handleSignUpClick}
          >
            Sign Up/Sign In
          </motion.button>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden">
          <motion.button
            className="text-gray-800"
            whileTap={{ scale: 0.9 }}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </motion.button>
        </div>
      </div>

      {/* Mobile Menu */}
      <AnimatePresence>
        {isMobileMenuOpen && (
          <motion.div 
            className="fixed inset-0 bg-white z-40 md:hidden"
            initial={{ opacity: 0, x: '100%' }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: '100%' }}
            transition={{ type: 'tween' }}
          >
            <div className="flex flex-col h-full pt-24 px-6 space-y-6">
              {navItems.map((item) => (
                <motion.button
                  key={item}
                  className="text-xl text-gray-800 text-center py-3 border-b border-gray-200"
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleClick(item)}
                >
                  {item}
                </motion.button>
              ))}
              <motion.button 
                className="px-8 py-3 rounded-xl bg-[#8b5cf6] text-white font-semibold text-lg"
                whileTap={{ scale: 0.95 }}
                onClick={handleSignUpClick}
              >
                Sign Up
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}

export default Navbar