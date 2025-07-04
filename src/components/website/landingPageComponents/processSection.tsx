import React from 'react'
import { UserCircle, CalendarCheck, FileSignature, Rocket, ChevronRight } from 'lucide-react'
import { useNavigate } from 'react-router-dom';

interface ProcessCardProps {
  step: string
  icon: React.ReactNode
  title: string
  description: string
}

const ProcessCard: React.FC<ProcessCardProps> = ({ step, icon, title, description }) => (
  <div className="bg-white p-6 rounded-3xl shadow-xl hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 relative group overflow-hidden border-2 border-transparent hover:border-[#8b5cf6] h-[270px]">
    <div className="absolute -top-4 -left-4 w-16 h-16 bg-[#8b5cf6] text-white rounded-full flex items-center justify-center font-bold text-xl shadow-lg transform group-hover:scale-110 transition-transform duration-300 z-10">
      {step}
    </div>
    <div className="w-16 h-16 bg-gradient-to-br from-[#8b5cf6] to-[#8b5cf6] text-white rounded-2xl flex items-center justify-center mb-3 transform group-hover:rotate-12 transition-transform duration-300 shadow-md">
      {React.cloneElement(icon as React.ReactElement, { className: "w-8 h-8" })}
    </div>
    <h3 className="text-lg font-bold mb-2 text-black group-hover:text-[#999999] transition-colors duration-300">{title}</h3>
    <p className="text-sm text-gray-700 leading-relaxed mb-3 opacity-80">{description}</p>
    <div className="flex items-center text-[#999999] group-hover:text-[#999999] transition-colors duration-300">
      <span className="text-sm font-semibold mr-1">Learn More</span>
      <ChevronRight className="w-4 h-4 transform group-hover:translate-x-1 transition-transform duration-300" />
    </div>
    <div className="absolute -bottom-2 -right-2 w-20 h-20 bg-[#8b5cf6] rounded-full opacity-10 group-hover:opacity-20 transition-opacity duration-300"></div>
  </div>
)

interface ProcessStep {
  step: string
  icon: React.ReactNode
  title: string
  description: string
}

const updatedSteps: ProcessStep[] = [
  {
    step: "1",
    icon: <UserCircle />,
    title: "Eligibility Check",
    description: "Ensure you meet the criteria to embark on this transformative journey with MPOVR.",
  },
  {
    step: "2",
    icon: <CalendarCheck />,
    title: "Application Process",
    description: "Submit your profile and schedule an expert consultation to assess your readiness.",
  },
  {
    step: "3",
    icon: <FileSignature />,
    title: "Enrollment & Agreement",
    description: "Finalize your enrollment and sign the training agreement to confirm your commitment.",
  },
  {
    step: "4",
    icon: <Rocket />,
    title: "Career Reskilling",
    description: "Engage in a 90-day intensive training to build in-demand Cloud ERP skills.",
  },
]

interface ProcessSectionProps {
  title?: string
  subtitle?: string
  steps?: ProcessStep[]
}

const ProcessSection: React.FC<ProcessSectionProps> = ({
  title = "MPOVR Training Enrollment Process",
  subtitle = "Your Second Chance Starts Here",
  steps = updatedSteps,
}) => {
  const navigate = useNavigate();
  function handleJourneyClick(){
    navigate('/apply')
}
  return (
    <section className="py-12 bg-white relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCI+CjxyZWN0IHdpZHRoPSI2MCIgaGVpZ2h0PSI2MCIgZmlsbD0iI2ZmZmZmZiI+PC9yZWN0Pgo8cGF0aCBkPSJNMzYgNDZjMCAyLjIwOS0xLjc5MSA0LTQgNHMtNC0xLjc5MS00LTQgMS43OTEtNCA0LTQgNCAxLjc5MSA0IDR6IiBmaWxsPSIjMzk5ZmM2IiBmaWxsLW9wYWNpdHk9IjAuMSI+PC9wYXRoPgo8L3N2Zz4=')] opacity-20"></div>
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-12">
          <span className="text-black bg-[#999999]/10 px-6 py-1.5 rounded-full text-sm font-semibold inline-block mb-3 shadow-sm">
            {subtitle}
          </span>
          <h2 className="text-4xl font-extrabold mt-4 text-black leading-tight bg-black bg-clip-text text-transparent">
            MPOVR Training Enrollment Process
          </h2>
          <p className="text-lg text-gray-600 mt-4 max-w-2xl mx-auto leading-relaxed">
            Targeted reskilling for individuals ready to step into high-demand Cloud ERP roles. Your second chance is now!
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
          <button className="px-8 py-4 bg-[#8b5cf6] text-white rounded-full font-semibold flex items-center gap-2 hover:bg-[#8b5cf6] inline-flex items-center group"
          onClick={handleJourneyClick}
          >
            Start Your Journey Today
            <ChevronRight className="ml-3 w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </section>
  )
}

export default ProcessSection
