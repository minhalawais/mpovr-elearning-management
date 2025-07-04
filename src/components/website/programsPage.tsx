'use client'

import React,{useEffect} from 'react'
import { motion } from 'framer-motion'
import Navbar from './landingPageComponents/navbar.tsx'
import { type LucideIcon } from 'lucide-react'
import { useNavigate } from 'react-router-dom';

import { Code, Database, Cloud, Globe, Shield, ChartBar, Briefcase, DollarSign, Users, LineChart } from 'lucide-react'

interface ProgramProps {
     id: number,
    title: string
  subtitle: string
  description: string
  icon: LucideIcon
  duration: string
  level: string
  features: string[]
}

interface ProgramCardProps {
  program: ProgramProps
  index: number
}

const ProgramCard: React.FC<ProgramCardProps> = ({ program, index }) => {
  const navigate = useNavigate();

  const handleLearnMore = (programId) => {
    navigate(`/program/${programId}`);
  };
  return (
    <motion.div 
      className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-200 hover:border-[#8b5cf6]/30 group"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.1 * index }}
    >
      <div className="flex items-start mb-4 space-x-4">
        <div className="w-14 h-14 rounded-xl bg-[#8b5cf6]/10 flex items-center justify-center shrink-0 group-hover:bg-[#8b5cf6]/20 transition-all duration-300">
          <program.icon className="w-7 h-7 text-[#8b5cf6] group-hover:scale-110 transition-transform duration-300" />
        </div>
        <div>
          <h2 className="text-2xl font-bold text-gray-800 group-hover:text-[#8b5cf6] transition-colors duration-300">{program.title}</h2>
          <p className="text-[#8b5cf6] font-medium">{program.subtitle}</p>
        </div>
      </div>
      <p className="text-gray-600 mb-4 leading-relaxed">{program.description}</p>
      <div className="flex justify-between text-sm text-gray-500 mb-4 border-b border-gray-100 pb-4">
        <div className="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-[#8b5cf6]/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span>Duration: {program.duration}</span>
        </div>
        <div className="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-[#8b5cf6]/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
          </svg>
          <span>Level: {program.level}</span>
        </div>
      </div>
      <h3 className="font-semibold text-gray-700 mb-3 flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2 text-[#8b5cf6]/70" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4M7.835 4.697a3.42 3.42 0 001.946-.806 3.42 3.42 0 014.438 0 3.42 3.42 0 001.946.806 3.42 3.42 0 013.138 3.138 3.42 3.42 0 00.806 1.946 3.42 3.42 0 010 4.438 3.42 3.42 0 00-.806 1.946 3.42 3.42 0 01-3.138 3.138 3.42 3.42 0 00-1.946.806 3.42 3.42 0 01-4.438 0 3.42 3.42 0 00-1.946-.806 3.42 3.42 0 01-3.138-3.138 3.42 3.42 0 00-.806-1.946 3.42 3.42 0 010-4.438 3.42 3.42 0 00.806-1.946 3.42 3.42 0 013.138-3.138z" />
        </svg>
        Key Features
      </h3>
      <ul className="space-y-2 text-gray-600 mb-6">
        {program.features.map((feature, index) => (
          <li 
            key={index} 
            className="flex items-center space-x-2 before:content-['✓'] before:text-[#8b5cf6] before:mr-2 before:font-bold"
          >
            {feature}
          </li>
        ))}
      </ul>
      <motion.button
        className="w-full px-4 py-3 bg-[#8b5cf6] text-white rounded-lg font-semibold hover:bg-[#7c3aed] transition-all duration-300 flex items-center justify-center space-x-2 group"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => handleLearnMore(program.id)}
      >
        <span>Learn More</span>
        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
        </svg>
      </motion.button>
    </motion.div>
  )
}

const programs = [
  {
    id: 1,
    title: "Workday HCM",
    subtitle: "Master Human Capital Management",
    description: "Dive deep into Workday's Human Capital Management system. Learn to manage employee data, streamline HR processes, and leverage analytics for strategic workforce planning.",
    icon: Users,
    duration: "3 months",
    level: "Advanced",
    features: [
      "Employee lifecycle management",
      "Compensation and benefits administration",
      "Talent and performance management",
      "Workforce analytics and reporting"
    ]
  },
  {
    id: 2,
    title: "Workday Financial Management",
    subtitle: "Optimize financial operations",
    description: "Master Workday's financial management tools. Learn to streamline accounting processes, enhance financial reporting, and drive better business decisions through real-time financial insights.",
    icon: DollarSign,
    duration: "3 months",
    level: "Advanced",
    features: [
      "General ledger and accounting",
      "Accounts payable and receivable",
      "Financial reporting and analytics",
      "Budget and planning tools"
    ]
  },
  {
       id: 3,
    title: "Workday Integration",
    subtitle: "Connect Workday with enterprise systems",
    description: "Learn to integrate Workday with other enterprise systems. Master the tools and techniques for seamless data flow and process automation across your organization's technology ecosystem.",
    icon: Cloud,
    duration: "3 months",
    level: "Advanced",
    features: [
      "Workday Studio",
      "Enterprise Interface Builder (EIB)",
      "Workday Web Services",
      "Third-party integration tools"
    ]
  },
  {
       id: 4,
    title: "Workday Reporting and Analytics",
    subtitle: "Unlock data-driven insights",
    description: "Develop expertise in Workday's reporting and analytics capabilities. Learn to create powerful reports, dashboards, and predictive models to drive strategic decision-making.",
    icon: ChartBar,
    duration: "3 months",
    level: "Advanced",
    features: [
      "Custom report creation",
      "Dashboard design",
      "Advanced analytics and data modeling",
      "Workday Prism Analytics"
    ]
  },
  {
       id: 5,
    title: "Workday Security and Compliance",
    subtitle: "Ensure data protection and regulatory compliance",
    description: "Master Workday's security features and compliance tools. Learn to implement robust security measures and ensure your Workday implementation meets industry regulations and standards.",
    icon: Shield,
    duration: "3 months",
    level: "Advanced",
    features: [
      "Role-based access control",
      "Data privacy and protection",
      "Audit trails and compliance reporting",
      "Security administration"
    ]
  },
  {
       id: 6,
    title: "Workday Project and Work Management",
    subtitle: "Optimize project delivery and resource management",
    description: "Learn to leverage Workday's project and work management capabilities. Master tools for project planning, resource allocation, time tracking, and project financial management.",
    icon: Briefcase,
    duration: "3 months",
    level: "Advanced",
    features: [
      "Project planning and scheduling",
      "Resource management",
      "Time tracking and billing",
      "Project financial management"
    ]
  }
]

const ProgramsPage: React.FC = () => {
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
          Our Programs
        </motion.h1>
        <motion.p 
          className="text-xl text-center text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          Explore our comprehensive range of Workday programs designed to elevate your career in enterprise technology. Each program is crafted to provide you with the skills and knowledge demanded by top employers in the Workday ecosystem.
        </motion.p>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {programs.map((program, index) => (
            <ProgramCard key={index} program={program} index={index} />
          ))}
        </div>
      </div>
    </div>
  )
}

export default ProgramsPage