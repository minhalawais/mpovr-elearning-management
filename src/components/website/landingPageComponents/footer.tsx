import React from 'react';
import { motion } from 'framer-motion';
import { Globe, MessageSquare, Bell, ArrowRight, Clock, Shield, Users, Zap, FileText } from 'lucide-react';
import mpovrLogo from '../../../images/mpovr_logo.png'; // Updated import path


const Footer: React.FC = () => {
  return (
    <footer className="bg-white text-grey py-16 pb-4 relative overflow-hidden">
      {/* Enhanced Network Pattern Background */}
      <div className="absolute inset-0 opacity-5">
        <svg width="100%" height="100%" xmlns="http://www.w3.org/2000/svg">
          <defs>
            <pattern id="network" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
              <circle cx="50" cy="50" r="1" fill="#8b5cf6" />
              <circle cx="0" cy="0" r="1" fill="#8b5cf6" />
              <circle cx="0" cy="100" r="1" fill="#8b5cf6" />
              <circle cx="100" cy="0" r="1" fill="#8b5cf6" />
              <circle cx="100" cy="100" r="1" fill="#8b5cf6" />
              <line x1="50" y1="50" x2="0" y2="0" stroke="#8b5cf6" strokeWidth="0.5" />
              <line x1="50" y1="50" x2="0" y2="100" stroke="#8b5cf6" strokeWidth="0.5" />
              <line x1="50" y1="50" x2="100" y2="0" stroke="#8b5cf6" strokeWidth="0.5" />
              <line x1="50" y1="50" x2="100" y2="100" stroke="#8b5cf6" strokeWidth="0.5" />
            </pattern>
          </defs>
          <rect width="100%" height="100%" fill="url(#network)" />
        </svg>
      </div>
      
      <div className="container mx-auto px-6 relative z-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Logo and About */}
          <motion.div 
            className="space-y-6 bg-white p-6 rounded-2xl backdrop-blur-sm hover:bg-white transition-all duration-300 border border-white/10 shadow-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <h3 className="text-3xl font-bold flex items-center space-x-4">
                <img src={mpovrLogo} alt="MPOVR Logo" className="w-12 h-10" />
              <span className="tracking-wider bg-clip-text text-transparent bg-[#8b5cf6] Benzin-font ml-0" style={{marginLeft: '3px',marginTop: '12px'}}>mpovr</span>
            </h3>
            <p className="text-[#999999] text-sm leading-relaxed">
              Revolutionizing ERP Training for Career Transformation
            </p>
            <div className="flex space-x-4 pt-4 text-[#999999]">
              {[
                { icon: <Globe />, label: 'Website' },
                { icon: <MessageSquare />, label: 'Contact' },
                { icon: <Bell />, label: 'Notifications' }
              ].map((item, index) => (
                <motion.a 
                  key={index} 
                  href="#" 
                  aria-label={item.label}
                  className="w-10 h-10 rounded-full bg-white flex items-center justify-center hover:bg-[#8b5cf6] transition-all shadow-lg"
                  whileHover={{ scale: 1.1 }}
                >
                  {React.cloneElement(item.icon, { className: 'w-5 h-5' })}
                </motion.a>
              ))}
            </div>
          </motion.div>

          {/* ERP Programs */}
          <motion.div 
            className="bg-white p-6 rounded-2xl backdrop-blur-sm hover:bg-white transition-all duration-300 border border-white/10  shadow-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
          >
            <h4 className="font-semibold text-xl mb-6 text-black border-b border-white/20 pb-3">ERP Programs</h4>
            <ul className="space-y-4">
              {['SAP S/4HANA', 'Oracle Cloud ERP', 'Microsoft Dynamics 365', 'Workday'].map((program, index) => (
                <motion.li
                  key={index}
                  className="hover:text-[#8b5cf6] transition-colors group cursor-pointer flex items-center space-x-3"
                  whileHover={{ x: 5 }}
                >
                  <ArrowRight className="w-4 h-4 text-black opacity-0 group-hover:opacity-100 transition-opacity" />
                  <span>{program}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Platform Features */}
          <motion.div 
            className="bg-white p-6 rounded-2xl backdrop-blur-sm hover:bg-white transition-all duration-300 border border-white/10 shadow-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h4 className="font-semibold text-xl mb-6 text-black border-b border-white/20 pb-3">Platform Features</h4>
            <ul className="space-y-4">
              {[
                { name: 'Virtual Classrooms', icon: <Users className="w-5 h-5 text-black" /> },
                { name: 'Secure Environment', icon: <Shield className="w-5 h-5 text-black" /> },
                { name: 'Career Support', icon: <Zap className="w-5 h-5 text-black" /> },
                { name: 'Digital Agreements', icon: <FileText className="w-5 h-5 text-black" /> },
              ].map((feature, index) => (
                <motion.li
                  key={index}
                  className="hover:text-[#8b5cf6] transition-colors group cursor-pointer flex items-center space-x-3"
                  whileHover={{ x: 5 }}
                >
                  {feature.icon}
                  <span>{feature.name}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>

          {/* Connect With Us */}
          <motion.div 
            className="bg-white p-6 rounded-2xl backdrop-blur-sm hover:bg-white transition-all duration-300 border border-white/10 shadow-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <h4 className="font-semibold text-xl mb-6 text-black border-b border-white/20 pb-3">Connect With Us</h4>
            <ul className="space-y-4">
              {[
                { icon: <MessageSquare />, text: 'support@mpovr.com' },
                { icon: <Bell />, text: '+1 (555) 123-4567' },
                { icon: <Clock />, text: '24/7 Support Available' }
              ].map((contact, index) => (
                <motion.li 
                  key={index} 
                  className="flex items-center space-x-3 hover:text-[#8b5cf6] transition-colors group cursor-pointer"
                  whileHover={{ x: 5 }}
                >
                  {React.cloneElement(contact.icon, { className: 'w-5 h-5 text-black' })}
                  <span>{contact.text}</span>
                </motion.li>
              ))}
            </ul>
          </motion.div>
        </div>

        {/* Footer Bottom */}
        <motion.div 
          className="border-t border-white/20 mt-4 pt-4 text-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.6, delay: 0.4 }}
        >
          <p className="text-[#999999] text-sm">
            &copy; 2024 MPOVR. All rights reserved. | 
            <a 
              href="#" 
              className="hover:text-[#8b5cf6] ml-2 hover:underline transition-colors"
            >
              Privacy Policy
            </a> | 
            <a 
              href="#" 
              className="hover:text-[#8b5cf6] ml-2 hover:underline transition-colors"
            >
              Terms of Service
            </a>
          </p>
        </motion.div>
      </div>
    </footer>
  );
};

export default Footer;

