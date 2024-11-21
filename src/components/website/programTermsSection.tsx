import React from 'react'
import { UserCircle, Monitor, Shield, FileText, Zap, BarChart, ArrowRight } from 'lucide-react'

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
  additionalDetail?: string
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description, additionalDetail }) => (
  <div className="bg-white p-6 rounded-2xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border-b-4 border-transparent hover:border-[#E18400] relative group overflow-hidden h-[270px] flex flex-col justify-between">
    <div className="absolute -top-8 -right-8 w-32 h-32 bg-[#edf6f9] rounded-full opacity-40 group-hover:opacity-70 transition-all duration-300 transform group-hover:scale-125"></div>
    <div className="relative z-10 flex-grow">
      <div className="w-14 h-14 bg-gradient-to-br from-[#399fc6] to-[#3756C0] text-white rounded-2xl flex items-center justify-center mb-4 transform group-hover:rotate-6 transition-transform duration-300 shadow-md">
        {React.cloneElement(icon as React.ReactElement, { className: "w-6 h-6" })}
      </div>
      <h3 className="text-lg font-semibold mb-2 text-[#3756C0] group-hover:text-[#E18400] transition-colors duration-300">{title}</h3>
      <p className="text-sm text-gray-600 leading-relaxed mb-2">{description}</p>
      {additionalDetail && (
        <p className="text-xs text-[#399fc6] italic">{additionalDetail}</p>
      )}
    </div>
    <div className="mt-4 pt-2 border-t border-gray-100 flex items-center justify-between">
      <span className="text-sm font-medium text-[#3756C0]">Learn More</span>
      <ArrowRight className="w-4 h-4 text-[#E18400] opacity-0 group-hover:opacity-100 transform translate-x-1 group-hover:translate-x-0 transition-all duration-300" />
    </div>
  </div>
)

const features = [
  {
    icon: <UserCircle />,
    title: "Personalized Learning Experience",
    description: "Access your custom dashboard with adaptive learning paths and real-time progress tracking.",
    additionalDetail: "Tailored for professionals with 2+ years of experience"
  },
  {
    icon: <Monitor />,
    title: "Immersive Virtual Classrooms",
    description: "Engage in interactive live sessions and access pre-recorded content from industry experts.",
    additionalDetail: "Cutting-edge LMS with dynamic assessments"
  },
  {
    icon: <Shield />,
    title: "Secure Learning Environment",
    description: "Benefit from two-factor authentication and admin-moderated communications for a safe experience.",
    additionalDetail: "Anonymous usernames for privacy protection"
  },
  {
    icon: <FileText />,
    title: "Streamlined Enrollment",
    description: "Complete your application, schedule interviews, and sign agreements digitally with ease.",
    additionalDetail: "Integrated with DocuSign for paperless workflow"
  },
  {
    icon: <Zap />,
    title: "Career Transformation Support",
    description: "Receive comprehensive guidance, including mock interviews and resume optimization.",
    additionalDetail: "Placement assistance upon successful completion"
  },
  {
    icon: <BarChart />,
    title: "Advanced Analytics",
    description: "Track your progress with detailed analytics and receive periodic performance assessments.",
    additionalDetail: "Real-time insights for continuous improvement"
  }
]

interface ProgramFeaturesSectionProps {
  title?: string
  subtitle?: string
}

const ProgramFeaturesSection: React.FC<ProgramFeaturesSectionProps> = ({
  title = "Revolutionizing ERP Training",
  subtitle = "MPOVR Portal Features",
}) => {
  return (
    <section className="py-12 bg-gradient-to-b from-white to-[#edf6f9] relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-20"></div>
      <div className="container mx-auto px-6 relative z-10">
        <div className="text-center mb-12">
          <span className="text-[#399fc6] bg-[#399fc6]/10 px-4 py-1 rounded-full text-xs font-semibold inline-block mb-4 shadow-sm">
            {subtitle}
          </span>
          <h2 className="text-4xl font-bold mt-4 leading-tight text-[#3756C0]">
          Revolutionizing <span className="text-[#E18400] MontserratFont">ERP Training</span>
          </h2>
          <p className="text-base text-gray-600 mt-6 max-w-2xl mx-auto leading-relaxed">
            Experience a world-class ERP training platform designed to transform your professional journey with cutting-edge technology and unparalleled support.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <div key={index}>
              <FeatureCard 
                icon={feature.icon}
                title={feature.title}
                description={feature.description}
                additionalDetail={feature.additionalDetail}
              />
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <a href="#" className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-[#E18400] to-[#3756C0] text-white text-sm font-medium rounded-full transition-all duration-300 transform hover:scale-105 hover:shadow-md">
            Start Your ERP Journey Today
            <ArrowRight className="ml-2 w-4 h-4" />
          </a>
        </div>
      </div>
    </section>
  )
}

export default ProgramFeaturesSection
