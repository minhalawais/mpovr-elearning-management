import React from 'react'
import { 
  Clock, Heart, DollarSign, Calendar, CheckCircle, Shield, 
  BookOpen, Zap, Users, Briefcase 
} from 'lucide-react'

interface TermCardProps {
  icon: React.ReactNode
  title: string
  description: string
  additionalDetail?: string
}

const TermCard: React.FC<TermCardProps> = ({ icon, title, description, additionalDetail }) => (
  <div className="bg-[#edf6f9] p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700 group">
    <div className="flex items-start space-x-6">
      <div className="w-16 h-16 bg-[#006d77] text-white rounded-2xl flex items-center justify-center flex-shrink-0 transform group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <div>
        <h3 className="text-2xl font-bold mb-4 text-[#006d77] group-hover:text-[#83c5be] transition-colors">{title}</h3>
        <p className="text-gray-600 leading-relaxed">{description}</p>
        {additionalDetail && (
          <p className="text-sm text-[#83c5be] mt-2 italic">{additionalDetail}</p>
        )}
      </div>
    </div>
    <div className="mt-8 pt-6 border-t border-gray-200">
      <div className="flex items-center space-x-3 text-[#006d77]">
        <CheckCircle className="w-5 h-5" />
        <span className="text-sm font-medium">Flexible Options Available</span>
      </div>
    </div>
  </div>
)

interface Term {
  icon: React.ReactNode
  title: string
  description: string
  additionalDetail?: string
}

const defaultTerms: Term[] = [
  {
    icon: <Clock className="w-6 h-6" />,
    title: "Adaptive Timeline",
    description: "Complete your training within 18 months at your personalized pace",
    additionalDetail: "Modular learning paths tailored to individual progress"
  },
  {
    icon: <Heart className="w-6 h-6" />,
    title: "Comprehensive Support",
    description: "Dedicated assistance for medical emergencies with compassionate re-enrollment",
    additionalDetail: "Holistic student wellness program"
  },
  {
    icon: <DollarSign className="w-6 h-6" />,
    title: "Transparent Pricing",
    description: "Comprehensive, all-inclusive pricing with guaranteed no hidden costs",
    additionalDetail: "Flexible payment plans available"
  },
  {
    icon: <Shield className="w-6 h-6" />,
    title: "Academic Assurance",
    description: "18-month re-enrollment window for qualifying circumstances",
    additionalDetail: "Performance guarantee and success tracking"
  },
  {
    icon: <Users className="w-6 h-6" />,
    title: "Career Transition",
    description: "Targeted support for professionals seeking to enter high-growth IT careers",
    additionalDetail: "Comprehensive career guidance and placement assistance"
  },
  {
    icon: <Briefcase className="w-6 h-6" />,
    title: "Professional Prerequisites",
    description: "Designed for individuals with 2+ years of work experience and strong academic backgrounds",
    additionalDetail: "Rigorous candidate selection process"
  }
]

interface ProgramTermsSectionProps {
  title?: string
  subtitle?: string
  terms?: Term[]
  backgroundImage?: string
}

const ProgramTermsSection: React.FC<ProgramTermsSectionProps> = ({
  title = "Program Guidelines",
  subtitle = "Program Terms",
  terms = defaultTerms,
  backgroundImage = '',
}) => {
  return (
    <section className="py-24 bg-white relative overflow-hidden">
      {backgroundImage && (
        <div 
          className="absolute inset-0 opacity-5 bg-repeat z-0" 
          style={{ backgroundImage: `url(${backgroundImage})` }}
        ></div>
      )}
      <div className="container mx-auto px-6 relative z-10">
        <div className="text-center mb-20">
          <span className="text-[#006d77] bg-[#006d77]/10 px-4 py-2 rounded-full text-sm font-medium">
            {subtitle}
          </span>
          <h2 className="text-4xl font-bold mt-6 text-[#006d77]">{title}</h2>
          <p className="mt-4 text-gray-600 max-w-2xl mx-auto">
            Our comprehensive program is designed to provide flexibility, support, and an exceptional learning experience for career-driven professionals.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12">
          {terms.map((term, index) => (
            <TermCard 
              key={index}
              icon={term.icon}
              title={term.title}
              description={term.description}
              additionalDetail={term.additionalDetail}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default ProgramTermsSection