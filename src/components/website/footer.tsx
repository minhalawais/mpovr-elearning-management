import React from 'react';
import { 
  Globe, 
  MessageSquare, 
  Bell, 
  ArrowRight, 
  BookOpen, 
  Clock 
} from 'lucide-react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-[#006d77] text-white py-16 relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('')] opacity-5"></div>
      <div className="container mx-auto px-6 relative">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12">
          {/* Logo and About */}
          <div className="space-y-4">
            <h3 className="text-2xl font-bold flex items-center space-x-3">
              <Globe className="w-6 h-6" />
              <span>MPOVR Training</span>
            </h3>
            <p className="text-gray-300">Transforming careers, building futures</p>
            <div className="flex space-x-4 pt-4">
              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer">
                <Globe className="w-5 h-5" />
              </div>
              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer">
                <MessageSquare className="w-5 h-5" />
              </div>
              <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center hover:bg-white/20 transition-colors cursor-pointer">
                <Bell className="w-5 h-5" />
              </div>
            </div>
          </div>

          {/* Training Programs */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Training Programs</h4>
            <ul className="space-y-4">
              {['Cloud Computing', 'Data Science', 'DevOps', 'Cybersecurity'].map((program, index) => (
                <li
                  key={index}
                  className="hover:text-[#83c5be] transition-colors cursor-pointer flex items-center space-x-2"
                >
                  <ArrowRight className="w-4 h-4" />
                  <span>{program}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Resources</h4>
            <ul className="space-y-4">
              {['Alumni Stories', 'Tech Blog', 'Career Guide', 'Help Center'].map((resource, index) => (
                <li
                  key={index}
                  className="hover:text-[#83c5be] transition-colors cursor-pointer flex items-center space-x-2"
                >
                  <BookOpen className="w-4 h-4" />
                  <span>{resource}</span>
                </li>
              ))}
            </ul>
          </div>

          {/* Connect With Us */}
          <div>
            <h4 className="font-semibold text-lg mb-6">Connect With Us</h4>
            <ul className="space-y-4">
              <li className="flex items-center space-x-3">
                <MessageSquare className="w-5 h-5 text-[#83c5be]" />
                <span>admissions@mpovr.com</span>
              </li>
              <li className="flex items-center space-x-3">
                <Bell className="w-5 h-5 text-[#83c5be]" />
                <span>+1 (555) 123-4567</span>
              </li>
              <li className="flex items-center space-x-3">
                <Clock className="w-5 h-5 text-[#83c5be]" />
                <span>Mon - Sat: 9:00 AM - 6:00 PM</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Footer Bottom */}
        <div className="border-t border-white/20 mt-12 pt-8 text-center">
          <p className="text-gray-300">&copy; 2024 MPOVR Training. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
