import React from 'react';
import { Globe, MessageSquare, Bell, ArrowRight, Clock, Shield, Users, Zap, FileText } from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-gradient-to-br from-[#3756C0] to-[#399fc6] text-white py-16 pb-4 relative overflow-hidden">
      <div className="absolute inset-0 opacity-10 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')]"></div>
      
      <div className="container mx-auto px-6 relative">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Logo and About */}
          <div className="space-y-6 bg-white/10 p-6 rounded-2xl backdrop-blur-sm hover:bg-white/15 transition-all duration-300">
            <h3 className="text-3xl font-bold flex items-center space-x-4">
              <Globe className="w-8 h-8 text-[#E18400] animate-pulse" />
              <span className="tracking-wider">MPOVR</span>
            </h3>
            <p className="text-[#edf6f9] text-opacity-90 text-sm leading-relaxed">
              Revolutionizing ERP Training for Career Transformation
            </p>
            <div className="flex space-x-4 pt-4">
              {[
                { icon: <Globe />, label: 'Website' },
                { icon: <MessageSquare />, label: 'Contact' },
                { icon: <Bell />, label: 'Notifications' }
              ].map((item, index) => (
                <a 
                  key={index} 
                  href="#" 
                  aria-label={item.label}
                  className="w-12 h-12 rounded-full bg-white/20 flex items-center justify-center hover:bg-[#E18400] hover:scale-110 transition-all transform"
                >
                  {React.cloneElement(item.icon, { className: 'w-6 h-6' })}
                </a>
              ))}
            </div>
          </div>

          {/* ERP Programs */}
          <div className="bg-white/10 p-6 rounded-2xl backdrop-blur-sm hover:bg-white/15 transition-all duration-300">
            <h4 className="font-semibold text-xl mb-6 text-[#E18400] border-b border-white/20 pb-3">ERP Programs</h4>
            <ul className="space-y-4">
              {['SAP S/4HANA', 'Oracle Cloud ERP', 'Microsoft Dynamics 365', 'Workday'].map((program, index) => (
                <li
                  key={index}
                  className="hover:text-[#E18400] transition-colors group cursor-pointer flex items-center space-x-3"
                >
                  <ArrowRight className="w-5 h-5 text-[#e5e7eb] group-hover:translate-x-1 transition-transform" />
                  <span className="group-hover:pl-2 transition-all">{program}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Platform Features */}
          <div className="bg-white/10 p-6 rounded-2xl backdrop-blur-sm hover:bg-white/15 transition-all duration-300">
            <h4 className="font-semibold text-xl mb-6 text-[#E18400] border-b border-white/20 pb-3">Platform Features</h4>
            <ul className="space-y-4">
              {[
                { name: 'Virtual Classrooms', icon: <Users className="w-5 h-5 text-[#e5e7eb]" /> },
                { name: 'Secure Environment', icon: <Shield className="w-5 h-5 text-[#e5e7eb]" /> },
                { name: 'Career Support', icon: <Zap className="w-5 h-5 text-[#e5e7eb]" /> },
                { name: 'Digital Agreements', icon: <FileText className="w-5 h-5 text-[#e5e7eb]" /> },
              ].map((feature, index) => (
                <li
                  key={index}
                  className="hover:text-[#E18400] transition-colors group cursor-pointer flex items-center space-x-3"
                >
                  {feature.icon}
                  <span className="group-hover:pl-2 transition-all">{feature.name}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Connect With Us */}
          <div className="bg-white/10 p-6 rounded-2xl backdrop-blur-sm hover:bg-white/15 transition-all duration-300">
            <h4 className="font-semibold text-xl mb-6 text-[#E18400] border-b border-white/20 pb-3">Connect With Us</h4>
            <ul className="space-y-4">
              {[
                { icon: <MessageSquare />, text: 'support@mpovr.com' },
                { icon: <Bell />, text: '+1 (555) 123-4567' },
                { icon: <Clock />, text: '24/7 Support Available' }
              ].map((contact, index) => (
                <li 
                  key={index} 
                  className="flex items-center space-x-3 hover:text-[#E18400] transition-colors group cursor-pointer"
                >
                  {React.cloneElement(contact.icon, { className: 'w-5 h-5 text-[#e5e7eb] group-hover:rotate-6 transition-transform' })}
                  <span className="group-hover:pl-2 transition-all">{contact.text}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="border-t border-white/20 mt-12 pt-8 text-center">
          <p className="text-[#edf6f9] text-sm">
            &copy; 2024 MPOVR. All rights reserved. | 
            <a 
              href="#" 
              className="hover:text-[#E18400] ml-2 hover:underline transition-colors"
            >
              Privacy Policy
            </a> | 
            <a 
              href="#" 
              className="hover:text-[#E18400] ml-2 hover:underline transition-colors"
            >
              Terms of Service
            </a>
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;