import React from 'react'
import { ClipboardCheck, Calendar, FileCheck, Zap } from 'lucide-react'

interface ProcessCardProps {
  step: string
  icon: React.ReactNode
  title: string
  description: string
}

const ProcessCard: React.FC<ProcessCardProps> = ({ step, icon, title, description }) => (
  <div className="bg-[#edf6f9] p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2 relative animate-on-scroll opacity-0 translate-y-8 transition-all duration-700 group">
    <div className="absolute -top-4 -left-4 w-12 h-12 bg-[#006d77] text-white rounded-full flex items-center justify-center font-bold shadow-lg transform group-hover:scale-110 transition-transform">
      {step}
    </div>
    <div className="w-16 h-16 bg-[#006d77] text-white rounded-2xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-4 text-[#006d77] group-hover:text-[#83c5be] transition-colors">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
    <div className="absolute -bottom-3 -right-3 w-6 h-6 bg-[#83c5be] rounded-full hidden md:block transform group-hover:scale-150 transition-transform"></div>
  </div>
)

interface ProcessStep {
  step: string
  icon: React.ReactNode
  title: string
  description: string
}

const defaultSteps: ProcessStep[] = [
  {
    step: "1",
    icon: <ClipboardCheck className="w-6 h-6" />,
    title: "Quick Registration",
    description: "5-minute online registration with minimal documentation",
  },
  {
    step: "2",
    icon: <Calendar className="w-6 h-6" />,
    title: "Personal Interview",
    description: "Brief chat to understand your goals and aspirations",
  },
  {
    step: "3",
    icon: <FileCheck className="w-6 h-6" />,
    title: "Secure Enrollment",
    description: "Simple agreement and flexible payment options",
  },
  {
    step: "4",
    icon: <Zap className="w-6 h-6" />,
    title: "Begin Learning",
    description: "Start your transformation journey on your schedule",
  },
]

interface ProcessSectionProps {
  title?: string
  subtitle?: string
  steps?: ProcessStep[]
  backgroundImage?: string
}

const ProcessSection: React.FC<ProcessSectionProps> = ({
  title = "Your Journey to Success",
  subtitle = "Simple Steps",
  steps = defaultSteps,
  backgroundImage = '',
}) => {
  return (
    <section className="py-24 bg-white relative overflow-hidden">
      {backgroundImage && (
        <div 
          className="absolute inset-0 opacity-5 bg-repeat" 
          style={{ backgroundImage: `url(${backgroundImage})` }}
        ></div>
      )}
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-20">
          <span className="text-[#006d77] bg-[#006d77]/10 px-4 py-2 rounded-full text-sm font-medium">
            {subtitle}
          </span>
          <h2 className="text-4xl font-bold mt-6 text-[#006d77]">{title}</h2>
        </div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8 md:gap-12">
          {steps.map((step, index) => (
            <ProcessCard 
              key={index}
              step={step.step}
              icon={step.icon}
              title={step.title}
              description={step.description}
            />
          ))}
        </div>
      </div>
    </section>
  )
}

export default ProcessSection