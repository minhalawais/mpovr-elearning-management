'use client'

import React, { useEffect, useRef } from 'react'
import { Users, Trophy, Briefcase, DollarSign } from 'lucide-react'
import theme from "../theme"; // Adjust the path as needed

interface StatCardProps {
  number: string
  label: string
  icon: React.ReactNode
}

const StatCard: React.FC<StatCardProps> = ({ number, label, icon }) => {
  const cardRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in')
          }
        })
      },
      { threshold: 0.1 }
    )

    if (cardRef.current) {
      observer.observe(cardRef.current)
    }

    return () => {
      if (cardRef.current) {
        observer.unobserve(cardRef.current)
      }
    }
  }, [])

  return (
    <div
      ref={cardRef}
      className="text-center p-6 opacity-0 translate-y-8 transition-all duration-700 bg-white rounded-3xl shadow-lg hover:shadow-xl transform hover:-translate-y-2 relative group"
    >
      <div className="absolute inset-0 bg-gradient-to-br from-[#006d77]/10 to-[#83c5be]/10 rounded-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
      <div className="w-16 h-16 mx-auto mb-4 bg-[#006d77]/10 rounded-full flex items-center justify-center text-[#006d77] group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <h3 className="text-4xl font-bold text-[#006d77] mb-2 group-hover:scale-105 transition-transform duration-300">
        {number}
      </h3>
      <p className="text-gray-600 text-sm">{label}</p>
    </div>
  )
}

interface StatsData {
  number: string
  label: string
  icon: React.ReactNode
}

const defaultStats: StatsData[] = [
  {
    number: "10k+",
    label: "Alumni Worldwide",
    icon: <Users className="w-6 h-6" />,
  },
  {
    number: "96%",
    label: "Success Rate",
    icon: <Trophy className="w-6 h-6" />,
  },
  {
    number: "150+",
    label: "Corporate Partners",
    icon: <Briefcase className="w-6 h-6" />,
  },
  {
    number: "2x",
    label: "Average Salary Jump",
    icon: <DollarSign className="w-6 h-6" />,
  },
]

interface StatsProps {
  stats?: StatsData[]
  backgroundImage?: string
}

const StatsSection: React.FC<StatsProps> = ({ stats = defaultStats, backgroundImage = '/placeholder.svg?height=1080&width=1920' }) => {
  const headingRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('animate-in')
          }
        })
      },
      { threshold: 0.1 }
    )

    if (headingRef.current) {
      observer.observe(headingRef.current)
    }

    return () => {
      if (headingRef.current) {
        observer.unobserve(headingRef.current)
      }
    }
  }, [])

  return (
    <section className="py-24 bg-gradient-to-b from-white to-[#83c5be]/10 relative overflow-hidden">
      <div 
        className="absolute inset-0 opacity-5 bg-repeat mix-blend-multiply"
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>
      <div className="container mx-auto px-6 relative z-10">
        <div 
          ref={headingRef}
          className="text-center mb-16 opacity-0 translate-y-8 transition-all duration-700"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-[#006d77] mb-4">
            Empowering IT Careers
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            MPOVR is dedicated to helping individuals transition into high-growth global IT careers. 
            Our program is designed for those with work experience and a strong academic background, 
            providing the skills and support needed to succeed in the tech industry.
          </p>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <StatCard 
              key={index}
              number={stat.number}
              label={stat.label}
              icon={stat.icon}
            />
          ))}
        </div>
      </div>
      <div className="absolute bottom-0 left-0 right-0 h-24 bg-gradient-to-t from-white to-transparent"></div>
    </section>
  )
}

export default StatsSection