import React from 'react'
import { UserCheck, Video, Award, Rocket, Lock, BookOpen } from 'lucide-react'

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => (
  <div className="bg-white p-6 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border-2 border-transparent hover:border-[#8b5cf6] relative group overflow-hidden h-[220px] flex flex-col">
    <div className="absolute -top-4 -right-4 w-16 h-16 bg-[#8b5cf6] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
    <div className="w-12 h-12 bg-gradient-to-br from-[#8b5cf6] to-[#8b5cf6] text-white rounded-2xl flex items-center justify-center mb-4 transform group-hover:rotate-12 transition-transform">
      {React.cloneElement(icon as React.ReactElement, { className: "w-6 h-6" })}
    </div>
    <h3 className="text-lg font-bold mb-2 text-black group-hover:text-[#999999] transition-colors duration-300">{title}</h3>
    <p className="text-sm text-gray-700 leading-relaxed opacity-80 flex-grow">{description}</p>
    <div className="absolute -bottom-2 -left-2 w-12 h-12 bg-[#8b5cf6] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
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
    title: "Targeted Career Reskilling",
    description: "Specialized programs designed to build in-demand Cloud ERP skills, tailored for professionals seeking a second chance in their careers.",
  },
  {
    icon: <Video />,
    title: "Interactive Virtual Learning",
    description: "Engage in dynamic virtual classrooms and hands-on ERP simulations, equipping you with practical, job-ready skills.",
  },
  {
    icon: <Award />,
    title: "Career Transformation Support",
    description: "Comprehensive career guidance including eligibility checks, mock interviews, and strategic job placements.",
  },
  {
    icon: <Rocket />,
    title: "90-Day Intensive Practicum",
    description: "Focused, immersive training designed to build expertise in ERP systems, preparing you for industry roles within 90 days.",
  },
  {
    icon: <Lock />,
    title: "Safe and Secure Learning",
    description: "Two-factor authentication, anonymous usernames, and a monitored environment ensure a secure and focused learning experience.",
  },
  {
    icon: <BookOpen />,
    title: "Personalized Learning Path",
    description: "Tailored curriculum based on your background and career goals, ensuring an efficient and effective learning journey.",
  }
]

interface FeaturesSectionProps {
  title?: string
  subtitle?: string
  features?: Feature[]
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({
  title = "Discover How MPOVR Empowers You with Innovation",
  subtitle = "MPOVR's Features That Drive Your Success",
  features = defaultFeatures,
}) => {
  return (
    <section className="py-12 bg-white relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-20"></div>
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-12">
          <span className="text-black bg-[#399fc6]/10 px-6 py-1.5 rounded-full text-sm font-semibold inline-block mb-3 shadow-sm">
            {subtitle}
          </span>
          <h2 className="text-4xl font-extrabold mt-4 text-black leading-tight bg-black  bg-clip-text text-transparent">
            Step Into the Future with MPOVR's Career-Boosting Tools
          </h2>
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

