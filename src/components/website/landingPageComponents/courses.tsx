import React from 'react';
import { ArrowRight, Users, Database, Cloud, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';

export default function TopCoursesSection() {
  const navigate = useNavigate();
  const handleExploreProgramsClick = () => {
    navigate('/programs');
  };

  return (
    <section className="py-16 bg-[#eeebfe] relative overflow-hidden">
      {/* Subtle Network Pattern Background */}
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
        <motion.div
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="text-black bg-[#8b5cf6]/10 px-6 py-2 rounded-full text-sm font-semibold inline-block mb-4 shadow-sm">
            Our ERP & Workday Programs
          </span>
          <h2 className="text-4xl md:text-5xl font-bold mt-4 leading-tight text-gray-900">
            Accelerate Your ERP Career
          </h2>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto leading-relaxed">
            Choose from our industry-leading ERP and Workday practicum learning programs designed to propel your career to new heights
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <CourseCard
            title="Workday HCM Essentials"
            description="Dive into Workday's Human Capital Management system. Learn to navigate and utilize Workday HCM for efficient workforce management and HR processes."
            features={[
              'Workday HCM architecture overview',
              'Employee lifecycle management',
              'Compensation and benefits administration',
              'Reporting and analytics in Workday',
              'Integration with other Workday modules',
              'Best practices for HCM configuration'
            ]}
            icon={<Database className="w-8 h-8" />}
          />
          <CourseCard
            title="Workday Financials"
            description="Master Workday's financial management capabilities. This course covers everything from basic accounting to advanced financial reporting and analysis within the Workday ecosystem."
            features={[
              'General ledger and accounting setup',
              'Financial reporting and dashboards',
              'Budget and planning in Workday',
              'Accounts payable and receivable processes',
              'Asset management and depreciation',
              'Financial control and compliance features'
            ]}
            icon={<Cloud className="w-8 h-8" />}
          />
          <CourseCard
            title="Workday Integration Specialist"
            description="Become proficient in integrating Workday with other enterprise systems. Learn to design, build, and maintain seamless integrations for optimal business processes."
            features={[
              'Workday Studio and Integration Cloud',
              'API and web services fundamentals',
              'Data conversion and migration strategies',
              'Testing and troubleshooting integrations',
              'Security considerations for integrations',
              'Performance tuning and optimization'
            ]}
            icon={<Users className="w-8 h-8" />}
          />
        </div>

        <motion.div
          className="text-center mt-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <button 
            className="px-8 py-4 bg-[#8b5cf6] text-white rounded-full font-semibold flex items-center gap-2 hover:bg-[#7c3aed] shadow-lg shadow-[#8b5cf6]/20 inline-flex group transition-all duration-300"
            onClick={handleExploreProgramsClick}
          >
            Explore All Programs
            <ArrowRight className="ml-2 w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </button>
        </motion.div>
      </div>
    </section>
  );
}

interface CourseCardProps {
  title: string;
  description: string;
  features: string[];
  icon: React.ReactNode;
}

const CourseCard: React.FC<CourseCardProps> = ({ title, description, features, icon }) => (
  <motion.div
    className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden group flex flex-col border border-gray-100"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
  >
    <div className="p-6 flex-grow">
      <div className="w-16 h-16 bg-gradient-to-br from-[#8b5cf6] to-[#7c3aed] text-white rounded-xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform duration-300 shadow-md">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-gray-900 group-hover:text-[#8b5cf6] transition-colors duration-300">{title}</h3>
      <p className="text-gray-600 mb-4 leading-relaxed text-sm">{description}</p>
      <div className="space-y-2 mb-4">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center text-gray-500 group/feature">
            <div className="w-1.5 h-1.5 bg-[#8b5cf6] rounded-full mr-2 flex-shrink-0"></div>
            <span className="text-sm group-hover/feature:text-[#8b5cf6] transition-colors duration-300">{feature}</span>
          </div>
        ))}
      </div>
    </div>
    <div className="bg-gray-50 p-4 flex justify-between items-center mt-auto">
      <span className="text-black font-semibold text-sm">Learn More</span>
      <ChevronRight className="w-5 h-5 text-black transform group-hover:translate-x-1 transition-transform duration-300" />
    </div>
  </motion.div>
);

