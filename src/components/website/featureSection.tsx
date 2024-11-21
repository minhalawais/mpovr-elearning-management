import React from 'react'
import { Video, Award, UserCheck, Rocket, Lock, CheckCircle } from 'lucide-react'

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => (
  <div className="bg-gradient-to-br from-white to-[#edf6f9] p-6 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border-2 border-transparent hover:border-[#399fc6] relative group overflow-hidden">
    <div className="absolute -top-4 -right-4 w-16 h-16 bg-[#E18400] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
    <div className="w-12 h-12 bg-gradient-to-br from-[#399fc6] to-[#3756C0] text-white rounded-2xl flex items-center justify-center mb-4 transform group-hover:rotate-12 transition-transform">
      {React.cloneElement(icon as React.ReactElement, { className: "w-6 h-6" })}
    </div>
    <h3 className="text-lg font-bold mb-2 text-[#3756C0] group-hover:text-[#E18400] transition-colors duration-300">{title}</h3>
    <p className="text-sm text-gray-700 leading-relaxed opacity-80">{description}</p>
    <div className="absolute -bottom-2 -left-2 w-12 h-12 bg-[#3756C0] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
  </div>
)

interface Feature {
  icon: React.ReactNode
  title: string
  description: string
}

const defaultFeatures: Feature[] = [
  {
    icon: <UserCheck />,
    title: "Personalized Learning Path",
    description: "Tailored ERP training with role-based dashboards, adaptive modules, and comprehensive skill development.",
  },
  {
    icon: <Video />,
    title: "Immersive Virtual Training",
    description: "Engage in interactive virtual classrooms, prerecorded expert sessions, and real-world ERP scenario simulations.",
  },
  {
    icon: <Award />,
    title: "Career Acceleration Program",
    description: "Comprehensive support including mock interviews, resume optimization, and strategic career placement assistance.",
  },
  {
    icon: <Rocket />,
    title: "Advanced Learning Ecosystem",
    description: "Access cutting-edge learning management system with dynamic assessments, quizzes, and continuous skill tracking.",
  },
  {
    icon: <Lock />,
    title: "Secure Learning Environment",
    description: "Two-factor authentication, anonymous usernames, and admin-moderated communications ensure a safe learning experience.",
  },
  {
    icon: <CheckCircle />,
    title: "Certification & Recognition",
    description: "Comprehensive certification process with periodic grading and eligibility for career support upon successful completion.",
  }
]

interface FeaturesSectionProps {
  title?: string
  subtitle?: string
  features?: Feature[]
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({
  title = "Transform Your ERP Learning Journey",
  subtitle = "Innovative Learning Ecosystem",
  features = defaultFeatures,
}) => {
  return (
    <section className="py-12 bg-gradient-to-b from-white to-[#edf6f9] relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-20"></div>
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-12">
          <span className="text-[#399fc6] bg-[#399fc6]/10 px-6 py-1.5 rounded-full text-sm font-semibold inline-block mb-3 shadow-sm">
            {subtitle}
          </span>
          <h2 className="text-4xl font-extrabold mt-4 text-[#3756C0] leading-tight bg-gradient-to-r from-[#3756C0] to-[#399fc6] bg-clip-text text-transparent">
          Transform Your <span className="text-[#E18400] MontserratFont">ERP Learning</span> Journey
          </h2>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto leading-relaxed">
            Empowering learners with a comprehensive, technology-driven ERP training platform designed for global success
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div key={index}>
              <FeatureCard 
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
              />
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection
