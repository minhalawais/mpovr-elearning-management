import React from 'react';
import { ArrowRight, BookOpen, Users, Shield, Globe, ChevronRight, CheckCircle, Calendar, CreditCard, GraduationCap } from 'lucide-react';
import { motion } from 'framer-motion';

export default function TopCoursesSection() {
  return (
    <section className="py-16 bg-gradient-to-b from-white to-[#edf6f9] relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI1IiBoZWlnaHQ9IjUiPgo8cmVjdCB3aWR0aD0iNSIgaGVpZ2h0PSI1IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9yZWN0Pgo8L3N2Zz4=')] opacity-30"></div>
      <div className="container mx-auto px-6 relative">
        <motion.div 
          className="text-center mb-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <span className="text-[#399fc6] bg-[#399fc6]/10 px-6 py-2 rounded-full text-sm font-semibold inline-block mb-4 shadow-sm">
            Our ERP Programs
          </span>
          <h2 className="text-4xl md:text-5xl font-bold mt-4 text-[#3756C0] leading-tight">
            Accelerate Your <span className="text-[#E18400] MontserratFont" >ERP Career</span>
          </h2>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto leading-relaxed">
            Choose from our industry-leading ERP practicum learning programs designed to propel your career to new heights
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <CourseCard
            title="ERP Fundamentals"
            description="Master the basics of Enterprise Resource Planning and lay a strong foundation for your career. This comprehensive program covers essential ERP concepts and practical applications."
            features={[
              'Personalized learning dashboard',
              'Interactive virtual classrooms',
              'Hands-on assignments and projects',
              'Industry-recognized certification',
              'Access to prerecorded sessions',
              'Regular progress assessments'
            ]}
            icon={<BookOpen className="w-8 h-8" />}
            steps={[
              { icon: CheckCircle, text: "Complete your learner profile" },
              { icon: Calendar, text: "Schedule a 15-minute interview" },
              { icon: CreditCard, text: "Secure your spot with easy payment" },
              { icon: GraduationCap, text: "Start your ERP learning journey" }
            ]}
          />
          <CourseCard
            title="Advanced ERP Implementation"
            description="Take your ERP skills to the next level. Learn to implement and customize ERP solutions for various business needs, and gain hands-on experience with real-world projects."
            features={[
              'Real-world implementation projects',
              'One-on-one trainer interactions',
              'Advanced industry certifications',
              'Customization and integration techniques',
              'Performance optimization strategies',
              'Change management principles'
            ]}
            icon={<Users className="w-8 h-8" />}
            steps={[
              { icon: CheckCircle, text: "Verify your ERP fundamentals" },
              { icon: Calendar, text: "Book an assessment interview" },
              { icon: CreditCard, text: "Confirm enrollment with secure payment" },
              { icon: GraduationCap, text: "Dive into advanced ERP concepts" }
            ]}
          />
          <CourseCard
            title="ERP Security & Compliance"
            description="Become an expert in ERP security protocols and regulatory compliance. This specialized program focuses on protecting enterprise data and ensuring adherence to industry standards."
            features={[
              'Two-factor authentication protocols',
              'Role-based access control implementation',
              'Privacy regulations and compliance',
              'Security audit procedures',
              'Incident response planning',
              'Continuous monitoring techniques'
            ]}
            icon={<Shield className="w-8 h-8" />}
            steps={[
              { icon: CheckCircle, text: "Confirm your ERP background" },
              { icon: Calendar, text: "Schedule a security aptitude test" },
              { icon: CreditCard, text: "Secure your position with payment" },
              { icon: GraduationCap, text: "Begin your security specialization" }
            ]}
          />
        </div>

        <motion.div 
          className="text-center mt-12"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <button className="bg-gradient-to-r from-[#E18400] to-[#3756C0] text-white px-8 py-3 rounded-full font-semibold hover:opacity-90 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl inline-flex items-center group">
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
  steps: { icon: React.ElementType; text: string }[];
}

const CourseCard: React.FC<CourseCardProps> = ({ title, description, features, icon, steps }) => (
  <motion.div 
    className="bg-white rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 overflow-hidden group flex flex-col"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
  >
    <div className="p-6 flex-grow">
      <div className="w-16 h-16 bg-gradient-to-br from-[#399fc6] to-[#3756C0] text-white rounded-xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform duration-300 shadow-lg">
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-[#3756C0] group-hover:text-[#E18400] transition-colors duration-300">{title}</h3>
      <p className="text-gray-600 mb-4 leading-relaxed text-sm">{description}</p>
      <div className="space-y-2 mb-4">
        {features.map((feature, index) => (
          <div key={index} className="flex items-center text-gray-700 group/feature">
            <Globe className="w-4 h-4 mr-2 text-[#399fc6] group-hover/feature:text-[#E18400] transition-colors duration-300 flex-shrink-0" />
            <span className="text-sm group-hover/feature:text-[#3756C0] transition-colors duration-300">{feature}</span>
          </div>
        ))}
      </div>
      <div className="border-t border-gray-200 pt-4 mt-4">
        <h4 className="text-sm font-semibold text-[#3756C0] mb-2">How to Get Started:</h4>
        <div className="space-y-2">
          {steps.map((step, index) => (
            <div key={index} className="flex items-center text-gray-600">
              <step.icon className="w-4 h-4 mr-2 text-[#E18400]" />
              <span className="text-xs">{step.text}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
    <div className="bg-gradient-to-r from-[#edf6f9] to-white p-4 flex justify-between items-center mt-auto">
      <span className="text-[#3756C0] font-semibold text-sm">Learn More</span>
      <ChevronRight className="w-5 h-5 text-[#E18400] transform group-hover:translate-x-1 transition-transform duration-300" />
    </div>
  </motion.div>
);

