import React from 'react'
import { motion } from 'framer-motion'
import { Rocket, Target, Zap, Users, Trophy, Lightbulb, ArrowRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom';

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
  benefits: string[]
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, benefits }) => (
  <motion.div 
    className="bg-white p-6 rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300 transform hover:-translate-y-2 border border-gray-100 hover:border-[#8b5cf6]/50 relative group overflow-hidden h-full flex flex-col justify-between"
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.5 }}
  >
    <div className="absolute -top-8 -right-8 w-32 h-32 bg-[#8b5cf6] rounded-full opacity-5 group-hover:opacity-10 transition-all duration-300 transform group-hover:scale-150"></div>
    <div className="relative z-10 flex-grow">
      <div className="w-14 h-14 bg-gradient-to-br from-[#8b5cf6] to-[#7c3aed] text-white rounded-2xl flex items-center justify-center mb-4 transform group-hover:rotate-6 transition-transform duration-300 shadow-lg">
        {React.cloneElement(icon as React.ReactElement, { className: "w-6 h-6" })}
      </div>
      <h3 className="text-lg font-semibold mb-2 text-gray-800 group-hover:text-[#8b5cf6] transition-colors duration-300">{title}</h3>
      <p className="text-sm text-gray-600 leading-relaxed mb-4">{description}</p>
      <ul className="space-y-2">
        {benefits.map((benefit, index) => (
          <li key={index} className="flex items-center text-gray-500 text-sm">
            <div className="w-1.5 h-1.5 bg-[#8b5cf6] rounded-full mr-2 flex-shrink-0"></div>
            {benefit}
          </li>
        ))}
      </ul>
    </div>
    <div className="mt-4 pt-2 border-t border-gray-200 flex items-center justify-between">
      <span className="text-sm font-medium text-[#999999]">Explore Feature</span>
      <ArrowRight className="w-4 h-4 text-[#999999] opacity-0 group-hover:opacity-100 transform translate-x-1 group-hover:translate-x-0 transition-all duration-300" />
    </div>
  </motion.div>
)

const features = [
  {
    icon: <Rocket />,
    title: "Accelerated Learning Paths",
    description: "Fast-track your ERP expertise with our intensive, focused programs.",
    benefits: [
      "90-day completion timeline",
      "Industry-aligned curriculum",
      "Hands-on projects and simulations"
    ]
  },
  {
    icon: <Target />,
    title: "Precision Skill Mapping",
    description: "Tailor your learning journey to match high-demand ERP roles.",
    benefits: [
      "AI-driven skill gap analysis",
      "Personalized module recommendations",
      "Real-time industry trend integration"
    ]
  },
  {
    icon: <Zap />,
    title: "Dynamic Learning Experience",
    description: "Engage with cutting-edge educational technology for maximum retention.",
    benefits: [
      "Interactive 3D ERP simulations",
      "Adaptive learning algorithms",
      "Gamified progress tracking"
    ]
  },
  {
    icon: <Users />,
    title: "Collaborative Cohort System",
    description: "Learn and grow alongside peers in a supportive, competitive environment.",
    benefits: [
      "Peer-to-peer learning sessions",
      "Group projects mirroring real work scenarios",
      "Alumni mentorship connections"
    ]
  },
  {
    icon: <Trophy />,
    title: "Career Launchpad",
    description: "Transition seamlessly from learning to earning in the ERP industry.",
    benefits: [
      "Mock interviews with industry veterans",
      "Portfolio development workshops",
      "Exclusive job placement assistance"
    ]
  },
  {
    icon: <Lightbulb />,
    title: "Continuous Innovation Track",
    description: "Stay at the forefront of ERP advancements long after program completion.",
    benefits: [
      "Lifetime access to course updates",
      "Quarterly trend analysis webinars",
      "Innovation challenges with industry partners"
    ]
  }
]

interface ProgramFeaturesSectionProps {
  title?: string
  subtitle?: string
}

const ProgramFeaturesSection: React.FC<ProgramFeaturesSectionProps> = ({
  title = "Reskill and Thrive in the",
  subtitle = "Program Highlights",
}) => {
  const navigate = useNavigate();
  function handleNavigate(){
    navigate('/apply');
  }
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
          <span className="text-black bg-[#8b5cf6]/10 px-4 py-1.5 rounded-full text-sm font-semibold inline-block mb-4 shadow-sm">
            {subtitle}
          </span>
          <h2 className="text-4xl md:text-5xl font-bold mt-4 leading-tight text-gray-900">
            {title} Modern Workforce
          </h2>
          <p className="text-lg text-gray-600 mt-6 max-w-4xl mx-auto leading-relaxed">
          Join a transformative platform that blends advanced learning technologies, personalized training, and career-focused solutions to help you thrive in the competitive world of ERP.
          </p>
        </motion.div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard 
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              benefits={feature.benefits}
            />
          ))}
        </div>
        <motion.div 
          className="mt-12 text-center"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <button 
            className="inline-flex items-center px-8 py-4 bg-[#8b5cf6] text-white rounded-full font-semibold hover:bg-[#7c3aed] transition-all duration-300 shadow-lg shadow-[#8b5cf6]/20 group"
            onClick={handleNavigate}
          >
            Launch Your ERP Career
            <ArrowRight className="ml-2 w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </button>
        </motion.div>
      </div>
    </section>
  )
}

export default ProgramFeaturesSection

