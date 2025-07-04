import React, { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useNavigate, useLocation } from 'react-router-dom'
import { Menu, X, Bell, User, ChevronDown } from 'lucide-react'
import mpovrLogo from '../../images/mpovr_logo.png'

const Navbar: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false)
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)
  const [isProfileDropdownOpen, setIsProfileDropdownOpen] = useState(false)
  const navigate = useNavigate()
  const location = useLocation()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleClick = (item: string) => {
    switch(item) {
      case 'Quizzes':
        navigate('/quizzes');
        break;
      case 'Assignments':
        navigate('/assignments');
        break;
      case 'Content':
        navigate('/content');
        break;
      case 'VirtualSessions':
        navigate('/virtual-sessions');
        break;
      default:
        navigate('/');
    }
    setIsMobileMenuOpen(false);
  }

  const handleProfileAction = (action: string) => {
    switch(action) {
      case 'view':
        navigate('/profile');
        break;
      case 'edit':
        navigate('/profile/edit');
        break;
      case 'signout':
        // Implement sign out logic here
        navigate('/login');
        break;
    }
    setIsProfileDropdownOpen(false);
  }

  const navItems = [
    'Quizzes',
    'Assignments',
    'Content',
    'VirtualSessions'
  ];

  const isActive = (path: string) => {
    if(path === 'VirtualSessions') {
      return location.pathname === `/virtual-sessions`;
    }
    return location.pathname === `/${path.toLowerCase()}`;
  }

  return (
    <nav className={`
      fixed top-0 left-0 right-0 z-50 transition-all duration-300 
      ${isScrolled ? 'bg-white shadow-lg' : 'bg-white'}
    `}>
      <div className="container mx-auto px-6 py-2 flex items-center justify-between">
        {/* Logo */}
        <motion.div 
          className="text-2xl font-bold flex items-center space-x-3 cursor-pointer"
          whileHover={{ scale: 1.05 }}
          onClick={() => navigate('/trainer')}
        >         
          <img src={mpovrLogo} alt="MPOVR Logo" className="w-12 h-10" />
          <span className="text-transparent font-bold text-3xl bg-clip-text bg-[#8B5CF6] Benzin-font ml-0" style={{ marginLeft: '3px', marginTop: '12px' }}>mpovr</span>
        </motion.div>
      
        {/* Desktop Navigation */}
        <div className="hidden md:flex items-center space-x-6">
          {navItems.map((item) => (
            <motion.button
              key={item}
              className={`text-sm font-medium transition-colors duration-200 ${
                isActive(item) 
                  ? 'text-[#8B5CF6] font-semibold' 
                  : 'text-gray-800 hover:text-[#399fc6]'
              }`}
              whileHover={{ scale: 1.1 }}
              onClick={() => handleClick(item)}
            >
              {item}
            </motion.button>
          ))}
          <motion.button
            className="text-gray-800 hover:text-[#399fc6]"
            whileHover={{ scale: 1.1 }}
          >
            <Bell size={20} />
          </motion.button>
          <div className="relative">
            <motion.button
              className="text-gray-800 hover:text-[#399fc6] flex items-center"
              whileHover={{ scale: 1.1 }}
              onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
            >
              <User size={20} />
              <ChevronDown size={16} className="ml-1" />
            </motion.button>
            {isProfileDropdownOpen && (
              <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1">
                <button onClick={() => handleProfileAction('view')} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">View Profile</button>
                <button onClick={() => handleProfileAction('edit')} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Edit Profile</button>
                <button onClick={() => handleProfileAction('signout')} className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left">Sign Out</button>
              </div>
            )}
          </div>
        </div>

        {/* Mobile Menu Toggle */}
        <div className="md:hidden flex items-center space-x-4">
          <motion.button
            className="text-gray-800"
            whileHover={{ scale: 1.1 }}
          >
            <Bell size={20} />
          </motion.button>
          <motion.button
            className="text-gray-800"
            whileHover={{ scale: 1.1 }}
            onClick={() => setIsProfileDropdownOpen(!isProfileDropdownOpen)}
          >
            <User size={20} />
          </motion.button>
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
                  className={`text-xl text-center py-3 border-b border-gray-200 ${
                    isActive(item)
                      ? 'text-[#8B5CF6] font-semibold'
                      : 'text-gray-800'
                  }`}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => handleClick(item)}
                >
                  {item}
                </motion.button>
              ))}
              <motion.button
                className="text-xl text-center py-3 border-b border-gray-200 text-gray-800"
                whileTap={{ scale: 0.95 }}
                onClick={() => handleProfileAction('view')}
              >
                View Profile
              </motion.button>
              <motion.button
                className="text-xl text-center py-3 border-b border-gray-200 text-gray-800"
                whileTap={{ scale: 0.95 }}
                onClick={() => handleProfileAction('edit')}
              >
                Edit Profile
              </motion.button>
              <motion.button
                className="text-xl text-center py-3 border-b border-gray-200 text-gray-800"
                whileTap={{ scale: 0.95 }}
                onClick={() => handleProfileAction('signout')}
              >
                Sign Out
              </motion.button>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </nav>
  )
}

export default Navbar

