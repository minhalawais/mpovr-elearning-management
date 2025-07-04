'use client'

import React, { useEffect } from 'react'
import { motion } from 'framer-motion'
import { useParams } from 'react-router-dom'
import Navbar from './landingPageComponents/navbar.tsx'
import { Users, Calendar, BookOpen, GraduationCap, Award, Clock, ChevronRight, DollarSign, Cloud, BarChartIcon as ChartBar, Shield, Briefcase } from 'lucide-react'
import { useNavigate } from 'react-router-dom';

interface TrainerProps {
  name: string
  role: string
  bio: string
  image: string
}

interface BatchProps {
  startDate: string
  duration: string
  schedule: string
  seats: number
}

interface ProgramProps {
  id: number
  title: string
  subtitle: string
  description: string
  icon: React.ElementType
  duration: string
  level: string
  features: string[]
  curriculum: {
    title: string
    topics: string[]
  }[]
  learningOutcomes: string[]
  prerequisites: string[]
  trainer: TrainerProps
  upcomingBatches: BatchProps[]
}

const programs: ProgramProps[] = [
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
    ],
    curriculum: [
      {
        title: "Foundations of Workday HCM",
        topics: ["Introduction to Workday HCM", "Core HCM data model", "Organizational structures"]
      },
      {
        title: "Employee Lifecycle Management",
        topics: ["Hiring and onboarding", "Position management", "Transfers and promotions", "Termination processes"]
      },
      {
        title: "Compensation and Benefits",
        topics: ["Compensation plans", "Benefits administration", "Leave management", "Payroll integration"]
      },
      {
        title: "Talent Management",
        topics: ["Performance reviews", "Goal setting", "Succession planning", "Learning management"]
      },
      {
        title: "Reporting and Analytics",
        topics: ["Standard reports", "Custom report creation", "Dashboards", "Workforce analytics"]
      }
    ],
    learningOutcomes: [
      "Configure and manage core HCM processes in Workday",
      "Implement best practices for employee lifecycle management",
      "Design and administer compensation and benefits programs",
      "Leverage Workday's talent management features for employee development",
      "Create insightful reports and analytics for data-driven HR decisions"
    ],
    prerequisites: [
      "Basic understanding of HR processes and terminology",
      "Familiarity with cloud-based software systems",
      "Analytical mindset and attention to detail",
      "Commitment to completing hands-on exercises and projects"
    ],
    trainer: {
      name: "Sarah Johnson",
      role: "Senior Workday HCM Consultant",
      bio: "Sarah has over 10 years of experience implementing Workday HCM for Fortune 500 companies. She is passionate about helping organizations leverage technology to transform their HR processes.",
      image: ""
    },
    upcomingBatches: [
      { startDate: "July 1, 2023", duration: "3 months", schedule: "Weekends", seats: 20 },
      { startDate: "August 15, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 15 },
      { startDate: "September 5, 2023", duration: "3 months", schedule: "Full-time", seats: 25 }
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
    ],
    curriculum: [
      {
        title: "Foundations of Workday Financial Management",
        topics: ["Introduction to Workday Financials", "Core financial data model", "Chart of accounts"]
      },
      {
        title: "General Ledger and Accounting",
        topics: ["Journal entries", "Account reconciliation", "Period close processes", "Multi-entity and multi-currency"]
      },
      {
        title: "Accounts Payable and Receivable",
        topics: ["Supplier management", "Invoice processing", "Payment processing", "Customer billing and collections"]
      },
      {
        title: "Financial Reporting",
        topics: ["Standard financial reports", "Custom report creation", "Financial dashboards", "Regulatory reporting"]
      },
      {
        title: "Budgeting and Planning",
        topics: ["Budget development", "Forecasting", "Scenario planning", "Budget vs. actual analysis"]
      }
    ],
    learningOutcomes: [
      "Configure and manage core financial processes in Workday",
      "Implement best practices for general ledger, AP, and AR",
      "Design and generate comprehensive financial reports",
      "Leverage Workday's budgeting and planning tools for financial forecasting",
      "Optimize financial operations for better decision-making"
    ],
    prerequisites: [
      "Basic understanding of accounting principles and financial processes",
      "Familiarity with ERP systems",
      "Analytical skills and attention to detail",
      "Commitment to completing hands-on exercises and projects"
    ],
    trainer: {
      name: "Michael Chen",
      role: "Senior Workday Financials Consultant",
      bio: "Michael has 12 years of experience implementing Workday Financials for global organizations. He specializes in optimizing financial processes and enhancing reporting capabilities.",
      image: "/placeholder.svg?height=200&width=200"
    },
    upcomingBatches: [
      { startDate: "July 15, 2023", duration: "3 months", schedule: "Weekends", seats: 18 },
      { startDate: "August 1, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 15 },
      { startDate: "September 10, 2023", duration: "3 months", schedule: "Full-time", seats: 20 }
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
    ],
    curriculum: [
      {
        title: "Integration Fundamentals",
        topics: ["Integration architecture", "Data mapping", "Integration security", "Integration testing"]
      },
      {
        title: "Workday Studio",
        topics: ["Studio basics", "Building integrations", "Debugging and troubleshooting", "Best practices"]
      },
      {
        title: "Enterprise Interface Builder (EIB)",
        topics: ["EIB concepts", "Creating EIB integrations", "Data transformation", "Error handling"]
      },
      {
        title: "Workday Web Services",
        topics: ["SOAP and REST APIs", "Authentication and security", "API exploration and testing", "Integration patterns"]
      },
      {
        title: "Third-party Integration Tools",
        topics: ["Dell Boomi", "MuleSoft", "Jitterbit", "Custom connectors"]
      }
    ],
    learningOutcomes: [
      "Design and implement Workday integrations using various tools",
      "Develop proficiency in Workday Studio for complex integrations",
      "Create efficient data flows using Enterprise Interface Builder",
      "Leverage Workday Web Services for real-time integrations",
      "Implement best practices for integration security and performance"
    ],
    prerequisites: [
      "Basic understanding of integration concepts",
      "Familiarity with XML, JSON, and web services",
      "Knowledge of Workday's data model",
      "Programming experience (Java or similar language) is beneficial"
    ],
    trainer: {
      name: "Alex Rodriguez",
      role: "Senior Workday Integration Specialist",
      bio: "Alex has been specializing in Workday integrations for 8 years, with expertise in connecting Workday to various enterprise systems. He has successfully led integration projects for Fortune 500 companies.",
      image: "/placeholder.svg?height=200&width=200"
    },
    upcomingBatches: [
      { startDate: "August 5, 2023", duration: "3 months", schedule: "Weekends", seats: 15 },
      { startDate: "September 1, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 12 },
      { startDate: "October 10, 2023", duration: "3 months", schedule: "Full-time", seats: 18 }
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
    ],
    curriculum: [
      {
        title: "Reporting Fundamentals",
        topics: ["Workday's reporting architecture", "Data sources and security", "Report types and use cases"]
      },
      {
        title: "Custom Report Creation",
        topics: ["Report design principles", "Advanced filtering and calculations", "Composite reporting", "Matrix reporting"]
      },
      {
        title: "Dashboard Design",
        topics: ["Dashboard planning and layout", "Interactive elements", "Data visualization best practices", "Performance optimization"]
      },
      {
        title: "Advanced Analytics",
        topics: ["Statistical analysis in Workday", "Predictive modeling", "Trend analysis and forecasting"]
      },
      {
        title: "Workday Prism Analytics",
        topics: ["Data integration and preparation", "Data discovery and visualization", "Machine learning capabilities", "Augmented analytics"]
      }
    ],
    learningOutcomes: [
      "Design and create complex custom reports in Workday",
      "Develop interactive and insightful dashboards",
      "Apply advanced analytics techniques for data-driven decision making",
      "Leverage Workday Prism Analytics for enhanced data insights",
      "Implement best practices for report performance and user adoption"
    ],
    prerequisites: [
      "Familiarity with Workday's data model",
      "Basic understanding of data analysis concepts",
      "Experience with Excel or similar tools",
      "Analytical mindset and attention to detail"
    ],
    trainer: {
      name: "Emily Watson",
      role: "Workday Analytics and Reporting Expert",
      bio: "Emily has 10 years of experience in business intelligence and analytics, with the last 6 years focused on Workday reporting. She has helped numerous organizations transform their reporting capabilities.",
      image: "/placeholder.svg?height=200&width=200"
    },
    upcomingBatches: [
      { startDate: "July 20, 2023", duration: "3 months", schedule: "Weekends", seats: 20 },
      { startDate: "August 15, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 15 },
      { startDate: "September 5, 2023", duration: "3 months", schedule: "Full-time", seats: 25 }
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
    ],
    curriculum: [
      {
        title: "Workday Security Model",
        topics: ["Security architecture", "Domain security", "Securable items", "Inheritance and propagation"]
      },
      {
        title: "Role-Based Access Control",
        topics: ["Security groups", "Role design", "Permission sets", "Conditional security"]
      },
      {
        title: "Data Privacy and Protection",
        topics: ["Data encryption", "Data masking", "GDPR compliance", "Data retention policies"]
      },
      {
        title: "Audit and Compliance",
        topics: ["Audit trail configuration", "Compliance reporting", "SOX compliance", "Security testing and validation"]
      },
      {
        title: "Security Administration",
        topics: ["Security setup and maintenance", "User provisioning and deprovisioning", "Single sign-on (SSO)", "Multi-factor authentication"]
      }
    ],
    learningOutcomes: [
      "Design and implement a comprehensive security model in Workday",
      "Configure role-based access control for optimal security and usability",
      "Implement data privacy measures in compliance with regulations like GDPR",
      "Set up and manage audit trails for compliance reporting",
      "Administer Workday security features effectively"
    ],
    prerequisites: [
      "Basic understanding of information security concepts",
      "Familiarity with Workday's architecture",
      "Knowledge of relevant compliance regulations (e.g., GDPR, SOX)",
      "Experience with enterprise software administration"
    ],
    trainer: {
      name: "David Secure",
      role: "Workday Security and Compliance Specialist",
      bio: "David has over 15 years of experience in IT security, with the last 8 years focused on Workday security implementations. He has helped numerous organizations achieve and maintain compliance with various regulations.",
      image: "/placeholder.svg?height=200&width=200"
    },
    upcomingBatches: [
      { startDate: "August 1, 2023", duration: "3 months", schedule: "Weekends", seats: 15 },
      { startDate: "September 15, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 12 },
      { startDate: "October 1, 2023", duration: "3 months", schedule: "Full-time", seats: 20 }
    ]
  },
  {
    id:6,
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
    ],
    curriculum: [
      {
        title: "Project Management Fundamentals",
        topics: ["Project lifecycle in Workday", "Project structures and hierarchies", "Project templates", "Project budgeting"]
      },
      {
        title: "Resource Management",
        topics: ["Resource pools", "Capacity planning", "Resource allocation", "Skills and competencies"]
      },
      {
        title: "Time Tracking and Billing",
        topics: ["Time entry configurations", "Approval workflows", "Billable vs. non-billable time", "Client billing"]
      },
      {
        title: "Project Financial Management",
        topics: ["Project costing", "Revenue recognition", "Project budgeting and forecasting", "Project profitability analysis"]
      },
      {
        title: "Reporting and Analytics",
        topics: ["Project status reporting", "Resource utilization reports", "Financial performance dashboards", "Project portfolio analytics"]
      }
    ],
    learningOutcomes: [
      "Configure and manage projects effectively in Workday",
      "Implement best practices for resource allocation and management",
      "Set up time tracking and billing processes for accurate project costing",
      "Leverage Workday's project financial management tools for improved profitability",
      "Create insightful project reports and analytics for decision-making"
    ],
    prerequisites: [
      "Basic understanding of project management concepts",
      "Familiarity with resource management principles",
      "Knowledge of project accounting fundamentals",
      "Experience with enterprise software systems"
    ],
    trainer: {
      name: "Jennifer Project",
      role: "Senior Workday Project Management Consultant",
      bio: "Jennifer has over 12 years of experience in project management, with 7 years specializing in Workday implementations. She has successfully led numerous Workday Project and Work Management deployments for various industries.",
      image: "/placeholder.svg?height=200&width=200"
    },
    upcomingBatches: [
      { startDate: "July 10, 2023", duration: "3 months", schedule: "Weekends", seats: 18 },
      { startDate: "August 20, 2023", duration: "3 months", schedule: "Weekday evenings", seats: 15 },
      { startDate: "September 15, 2023", duration: "3 months", schedule: "Full-time", seats: 22 }
    ]
  }
]

const IndividualProgramDetail: React.FC = () => {
    const navigate = useNavigate()
  const params = useParams()
  const programId = parseInt(params.programId as string, 10)
  const program = programs.find(p => p.id === programId)

  useEffect(() => {
    window.scrollTo(0, 0)
  }, [])

  if (!program) {
    return <div>Program not found</div>
  }

  const IconComponent = program.icon

  return (
    <div className="min-h-screen bg-[#ede9fe] relative overflow-hidden">
      <div className="absolute top-0 left-0 right-0 h-96 bg-[#8b5cf6]/10 to-transparent"></div>
      <Navbar />
      
      <div className="container mx-auto px-4 py-24 relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: "easeOut" }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-extrabold mb-4 text-transparent bg-clip-text bg-black drop-shadow-lg">
            {program.title}
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            {program.description}
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-8 mb-16">
          <motion.div 
            className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50 transform transition-all hover:scale-[1.02]"
            initial={{ opacity: 0, x: -50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <GraduationCap className="mr-3 text-[#8b5cf6]" />
              Program Overview
            </h2>
            <div className="grid grid-cols-2 gap-4 mb-6">
              <div className="bg-purple-50 rounded-xl p-4 flex items-center space-x-3">
                <Clock className="w-8 h-8 text-[#8b5cf6]" />
                <div>
                  <p className="text-xs text-gray-500">Duration</p>
                  <p className="font-semibold text-gray-700">{program.duration}</p>
                </div>
              </div>
              <div className="bg-purple-50 rounded-xl p-4 flex items-center space-x-3">
                <IconComponent className="w-8 h-8 text-[#8b5cf6]" />
                <div>
                  <p className="text-xs text-gray-500">Level</p>
                  <p className="font-semibold text-gray-700">{program.level}</p>
                </div>
              </div>
            </div>
            <h3 className="font-semibold text-gray-700 mb-4">Key Features</h3>
            <ul className="space-y-3">
              {program.features.map((feature, index) => (
                <li 
                  key={index} 
                  className="flex items-center text-gray-600 bg-purple-50 rounded-lg p-3"
                >
                  <ChevronRight className="mr-3 text-[#8b5cf6]" />
                  {feature}
                </li>
              ))}
            </ul>
          </motion.div>
          
          <motion.div 
            className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50 transform transition-all hover:scale-[1.02]"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2, ease: "easeOut" }}
          >
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <Award className="mr-3 text-[#8b5cf6]" />
              Learning Outcomes
            </h2>
            <ul className="space-y-4">
              {program.learningOutcomes.map((outcome, index) => (
                <li 
                  key={index} 
                  className="flex items-start bg-purple-50 p-4 rounded-xl text-gray-700"
                >
                  <span className="w-6 h-6 bg-[#8b5cf6]/20 text-[#8b5cf6] rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    {index + 1}
                  </span>
                  {outcome}
                </li>
              ))}
            </ul>
          </motion.div>
        </div>

        <motion.div 
          className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50 mb-16"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3, ease: "easeOut" }}
        >
          <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
            <BookOpen className="mr-3 text-[#8b5cf6]" />
            Curriculum Overview
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {program.curriculum.map((module, index) => (
              <div 
                key={index} 
                className="bg-purple-50 rounded-2xl p-6 transform transition-all hover:scale-105 hover:shadow-lg"
              >
                <h3 className="font-semibold text-lg mb-3 text-[#8b5cf6]">{module.title}</h3>
                <ul className="space-y-2 text-gray-600">
                  {module.topics.map((topic, topicIndex) => (
                    <li 
                      key={topicIndex} 
                      className="flex items-center"
                    >
                      <ChevronRight className="mr-2 text-[#8b5cf6] w-4 h-4" />
                      {topic}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div 
          className="grid md:grid-cols-2 gap-8 mb-16"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.4, ease: "easeOut" }}
        >
          <div className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <BookOpen className="mr-3 text-[#8b5cf6]" />
              Prerequisites
            </h2>
            <ul className="space-y-4">
              {program.prerequisites.map((prerequisite, index) => (
                <li 
                  key={index} 
                  className="flex items-start bg-purple-50 p-4 rounded-xl text-gray-700"
                >
                  <span className="w-6 h-6 bg-[#8b5cf6]/20 text-[#8b5cf6] rounded-full flex items-center justify-center mr-4 flex-shrink-0">
                    {index + 1}
                  </span>
                  {prerequisite}
                </li>
              ))}
            </ul>
          </div>

          <div className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50">
            <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
              <Users className="mr-3 text-[#8b5cf6]" />
              Meet Your Trainer
            </h2>
            <div className="flex items-center space-x-6 bg-purple-50 p-6 rounded-2xl">
              <img 
                src={program.trainer.image} 
                alt={program.trainer.name} 
                className="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg"
              />
              <div>
                <h3 className="text-xl font-semibold text-gray-800">{program.trainer.name}</h3>
                <p className="text-[#8b5cf6] font-medium mb-2">{program.trainer.role}</p>
                <p className="text-gray-600">{program.trainer.bio}</p>
              </div>
            </div>
          </div>
        </motion.div>

        <motion.div 
          className="bg-white rounded-3xl p-8 shadow-2xl border border-purple-50 mb-16"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.5, ease: "easeOut" }}
        >
          <h2 className="text-2xl font-bold mb-6 text-gray-800 flex items-center">
            <Calendar className="mr-3 text-[#8b5cf6]" />
            Upcoming Batches
          </h2>
          <div className="grid md:grid-cols-3 gap-6">
            {program.upcomingBatches.map((batch, index) => (
              <div 
                key={index} 
                className="bg-purple-50 rounded-2xl p-6 transform transition-all hover:scale-105 hover:shadow-lg"
              >
                <Calendar className="w-10 h-10 text-[#8b5cf6] mb-4" />
                <h3 className="font-semibold text-lg mb-2 text-gray-800">Batch {index + 1}</h3>
                <div className="space-y-2 text-gray-600">
                  <p><strong>Start Date:</strong> {batch.startDate}</p>
                  <p><strong>Duration:</strong> {batch.duration}</p>
                  <p><strong>Schedule:</strong> {batch.schedule}</p>
                  <p><strong>Available Seats:</strong> {batch.seats}</p>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        <motion.div 
          className="text-center"
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.6, ease: "easeOut" }}
        >
          <button 
          className="px-10 py-4 bg-[#8b5cf6] text-white rounded-full font-bold text-lg shadow-2xl hover:shadow-xl transform transition-all hover:scale-105 hover:-translate-y-1"
           onClick={() => navigate('/apply')}
           >
            Enroll Now
          </button>
        </motion.div>
      </div>
    </div>
  )
}

export default IndividualProgramDetail

