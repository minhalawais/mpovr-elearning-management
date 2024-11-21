import React from 'react'
import { UserCircle, CalendarCheck, FileSignature, Rocket, ChevronRight } from 'lucide-react'

interface ProcessCardProps {
  step: string
  icon: React.ReactNode
  title: string
  description: string
}

const ProcessCard: React.FC<ProcessCardProps> = ({ step, icon, title, description }) => (
  <div className="bg-gradient-to-br from-white to-[#edf6f9] p-6 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative group overflow-hidden border-2 border-transparent hover:border-[#399fc6] h-[270px]">
    <div className="absolute -top-4 -left-4 w-16 h-16 bg-[#3756C0] text-white rounded-full flex items-center justify-center font-bold text-xl shadow-lg transform group-hover:scale-110 transition-transform duration-300 z-10">
      {step}
    </div>
    <div className="w-16 h-16 bg-gradient-to-br from-[#399fc6] to-[#3756C0] text-white rounded-2xl flex items-center justify-center mb-3 transform group-hover:rotate-12 transition-transform duration-300 shadow-md">
      {React.cloneElement(icon as React.ReactElement, { className: "w-8 h-8" })}
    </div>
    <h3 className="text-lg font-bold mb-2 text-[#3756C0] group-hover:text-[#E18400] transition-colors duration-300">{title}</h3>
    <p className="text-sm text-gray-700 leading-relaxed mb-3 opacity-80">{description}</p>
    <div className="flex items-center text-[#399fc6] group-hover:text-[#E18400] transition-colors duration-300">
      <span className="text-sm font-semibold mr-1">Learn More</span>
      <ChevronRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300" />
    </div>
    <div className="absolute -bottom-2 -right-2 w-20 h-20 bg-[#E18400] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
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
    icon: <UserCircle />,
    title: "Profile Creation",
    description: "Craft your personalized profile with key details to launch your ERP transformation journey.",
  },
  {
    step: "2",
    icon: <CalendarCheck />,
    title: "Expert Consultation",
    description: "Reserve a focused 15-minute strategy session to align your ERP learning goals.",
  },
  {
    step: "3",
    icon: <FileSignature />,
    title: "Enrollment Confirmation",
    description: "Complete your digital enrollment with flexible, transparent payment pathways.",
  },
  {
    step: "4",
    icon: <Rocket />,
    title: "Learning Acceleration",
    description: "Unlock your custom dashboard, immersive virtual classrooms, and dynamic assignments.",
  },
]

interface ProcessSectionProps {
  title?: string
  subtitle?: string
  steps?: ProcessStep[]
}

const ProcessSection: React.FC<ProcessSectionProps> = ({
  title = "Your ERP Mastery Blueprint",
  subtitle = "Innovative Onboarding",
  steps = defaultSteps,
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
            Your <span className="text-[#E18400] MontserratFont">ERP Mastery</span> Blueprint
          </h2>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto leading-relaxed">
            Transform your ERP skills with our cutting-edge, personalized training ecosystem
          </p>
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-4 justify-between items-stretch gap-6">
          {steps.map((step, index) => (
            <div key={index}>
              <ProcessCard 
                step={step.step}
                icon={step.icon}
                title={step.title}
                description={step.description}
              />
            </div>
          ))}
        </div>
        <div className="mt-12 text-center">
          <button className="bg-gradient-to-r from-[#E18400] to-[#3756C0] text-white px-10 py-3 rounded-full font-bold hover:opacity-90 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl inline-flex items-center group">
            Launch Your ERP Journey
            <ChevronRight className="ml-3 w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </section>
  )
}

export default ProcessSection
