'use client'

import React, { useEffect, useState } from 'react'
import { ArrowRight, Globe, Trophy, Award, ChevronDown } from 'lucide-react'

const HeroSection: React.FC = () => {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }
    window.addEventListener('scroll', handleScroll)
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header className="bg-gradient-to-br from-[#006d77] via-[#3d9299] to-[#83c5be] text-white relative overflow-hidden min-h-screen flex flex-col">
      <div className="absolute inset-0 bg-[url('')] opacity-5 bg-repeat" />
      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent" />

      {/* Refined Navigation */}
      <nav className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${isScrolled ? 'bg-[#006d77]/90 backdrop-blur-md py-2 shadow-lg' : 'bg-transparent py-6'}`}>
        <div className="container mx-auto px-6 flex items-center justify-between">
          <div className="text-2xl font-bold flex items-center space-x-3 hover:scale-105 transition-transform cursor-pointer">
            <Globe className="w-8 h-8 animate-spin-slow" />
            <span className="bg-gradient-to-r from-white to-gray-100 bg-clip-text text-transparent">MPOVR Training</span>
          </div>
          <div className="space-x-8 hidden md:flex items-center">
            {['Programs', 'Eligibility', 'Process', 'Contact'].map((item) => (
              <button
                key={item}
                className="hover:text-gray-200 transition-colors relative group text-sm font-medium"
              >
                {item}
                <span className="absolute bottom-0 left-0 w-0 h-0.5 bg-white transition-all group-hover:w-full"></span>
              </button>
            ))}
            <button className="bg-white text-[#006d77] px-6 py-2 rounded-full font-semibold hover:bg-opacity-90 transition-all transform hover:scale-105 shadow-lg hover:shadow-xl text-sm">
              Apply Now
            </button>
          </div>
        </div>
      </nav>

      {/* Refined Hero Content */}
      <div className="container mx-auto px-6 py-24 flex-grow flex items-center relative z-10">
        <div className="flex flex-col md:flex-row items-center gap-16">
          <div className="md:w-1/2 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700">
            <div className="inline-block px-4 py-2 bg-white/10 backdrop-blur-md rounded-full text-sm mb-6 animate-bounce-subtle">
              🚀 Transform Your Career Today
            </div>
            <h1 className="text-5xl md:text-6xl font-bold mb-8 leading-tight">
              Launch Your Global
              <span className="bg-gradient-to-r from-white to-[#83c5be] bg-clip-text text-transparent block">
                IT Career Journey
              </span>
            </h1>
            <p className="text-xl mb-10 text-gray-100 leading-relaxed">
              Join over 10,000+ professionals who transformed their careers through MPOVR's industry-leading training programs. Get certified, get noticed, get hired.
            </p>
            <div className="space-x-6 mb-12">
              <button className="bg-white text-[#006d77] px-8 py-4 rounded-full font-semibold hover:bg-opacity-90 transition-all transform hover:scale-105 inline-flex items-center shadow-xl hover:shadow-2xl">
                Start Your Journey <ArrowRight className="ml-2 animate-bounce-x" />
              </button>
              <button className="border-2 border-white px-8 py-4 rounded-full font-semibold hover:bg-white hover:text-[#006d77] transition-all shadow-lg hover:shadow-xl">
                Explore Programs
              </button>
            </div>
            <div className="flex items-center space-x-6">
              <div className="flex -space-x-4">
                {[1, 2, 3, 4].map((i) => (
                  <img
                    key={i}
                    src={`/placeholder.svg?height=48&width=48&text=${i}`}
                    alt={`Alumni ${i}`}
                    className="w-12 h-12 rounded-full border-2 border-white bg-[#83c5be] shadow-lg transform hover:scale-110 transition-transform cursor-pointer"
                    style={{ zIndex: 4 - i }}
                  />
                ))}
              </div>
              <p className="text-sm bg-white/10 backdrop-blur-md px-4 py-2 rounded-full">
                Join 10,000+ successful alumni worldwide
              </p>
            </div>
          </div>

          {/* Refined Hero Image */}
          <div className="md:w-1/2 mt-10 md:mt-0 animate-on-scroll opacity-0 translate-x-8 transition-all duration-700 relative">
            <div className="relative group">
              <div className="absolute -inset-4 bg-gradient-to-r from-[#006d77] to-[#83c5be] rounded-2xl blur opacity-20 group-hover:opacity-40 animate-pulse transition-opacity duration-300"></div>
              <img
                src="/placeholder.svg?height=600&width=600&text=IT+Training"
                alt="IT Training"
                className="rounded-2xl shadow-2xl relative transform group-hover:scale-105 transition-transform duration-300"
              />
              <div className="absolute -bottom-8 -left-8 bg-white text-[#006d77] p-6 rounded-xl shadow-2xl transform hover:scale-110 transition-transform cursor-pointer">
                <div className="flex items-center space-x-3">
                  <Trophy className="w-8 h-8 text-[#006d77] animate-bounce-subtle" />
                  <div>
                    <p className="font-bold text-lg">96% Success Rate</p>
                    <p className="text-sm text-gray-600">Career Transition</p>
                  </div>
                </div>
              </div>
              <div className="absolute -top-6 -right-6 bg-white text-[#006d77] p-4 rounded-full shadow-2xl transform hover:scale-110 transition-transform cursor-pointer">
                <Award className="w-8 h-8 text-[#006d77] animate-pulse" />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Scroll Indicator */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 animate-bounce">
        <ChevronDown className="w-8 h-8 text-white opacity-50" />
      </div>
    </header>
  )
}

export default HeroSection