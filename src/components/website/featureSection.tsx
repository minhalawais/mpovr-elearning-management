import React from 'react'
import { Video, Award, Users } from 'lucide-react'

interface FeatureCardProps {
  icon: React.ReactNode
  title: string
  description: string
}

const FeatureCard: React.FC<FeatureCardProps> = ({ icon, title, description }) => (
  <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700 group">
    <div className="w-16 h-16 bg-[#006d77] text-white rounded-2xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-4 text-[#006d77] group-hover:text-[#83c5be] transition-colors">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
  </div>
)

interface Feature {
  icon: React.ReactNode
  title: string
  description: string
}

const defaultFeatures: Feature[] = [
  {
    icon: <Video className="w-6 h-6" />,
    title: "Industry Expert Training",
    description: "Learn from professionals with 10+ years of global IT experience",
  },
  {
    icon: <Award className="w-6 h-6" />,
    title: "Global Certifications",
    description: "All certification costs included - no hidden fees",
  },
  {
    icon: <Users className="w-6 h-6" />,
    title: "Career Launch Support",
    description: "Mock interviews, resume building, and placement assistance",
  },
]

interface FeaturesSectionProps {
  title?: string
  subtitle?: string
  features?: Feature[]
  backgroundImage?: string
}

const FeaturesSection: React.FC<FeaturesSectionProps> = ({
  title = "Why Choose MPOVR?",
  subtitle = "Why Choose Us",
  features = defaultFeatures,
  backgroundImage = '',
}) => {
  return (
    <section className="py-24 bg-gradient-to-br from-[#006d77] via-[#3d9299] to-[#83c5be] relative overflow-hidden">
      {backgroundImage && (
        <div 
          className="absolute inset-0 opacity-5 bg-repeat" 
          style={{ backgroundImage: `url(${backgroundImage})` }}
        ></div>
      )}
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-20">
          <span className="text-white bg-white/20 backdrop-blur-md px-4 py-2 rounded-full text-sm font-medium">
            {subtitle}
          </span>
          <h2 className="text-4xl font-bold mt-6 text-white">{title}</h2>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {features.map((feature, index) => (
            <FeatureCard 
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default FeaturesSection