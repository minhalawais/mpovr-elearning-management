import React, { useEffect } from 'react';
import { ArrowRight, BookOpen, Video, Users, Calendar, Award, MessageSquare, FileCheck, Bell, GraduationCap, ClipboardCheck, Clock, DollarSign, Briefcase, Heart, CheckCircle, Globe, Zap, Trophy } from 'lucide-react';
import TopCoursesSection from './courses.tsx'
import StatsSection from './statsSection.tsx'
import ProcessSection from './processSection.tsx';
import FeaturesSection from './featureSection.tsx';
import ProgramTermsSection from './programTermsSection.tsx'
import CTASection from './ctaSection.tsx';
import Footer from './footer.tsx';
import HeroSection from './header.tsx';
import FAQSection  from './faqSection.tsx';
const LandingPage = () => {
  useEffect(() => {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('animate-in');
        }
      });
    }, { threshold: 0.1 });

    document.querySelectorAll('.animate-on-scroll').forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  return (
    <div className="min-h-screen bg-[#edf6f9]">
      {/* Hero Section with enhanced gradient and pattern */}
      <HeroSection/>

      <StatsSection/>

      <TopCoursesSection/>

      <ProcessSection/>
      <FeaturesSection/>

      <ProgramTermsSection/>

      
      <FAQSection/>
      <CTASection/>

      <Footer/>
    </div>
  );
};




// Enhanced Eligibility Card Component
const EligibilityCard = ({ icon, title, description }) => (
  <div className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2 animate-on-scroll opacity-0 translate-y-8 transition-all duration-700 group relative">
    <div className="absolute inset-0 bg-gradient-to-br from-[#006d77]/5 to-[#83c5be]/5 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity"></div>
    <div className="w-16 h-16 bg-[#006d77] text-white rounded-2xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-4 text-[#006d77]">{title}</h3>
    <p className="text-gray-600 leading-relaxed mb-6">{description}</p>
    <button className="text-[#006d77] font-semibold inline-flex items-center group-hover:text-[#83c5be] transition-colors">
      Learn More 
      <ArrowRight className="ml-2 w-4 h-4 transform group-hover:translate-x-1 transition-transform" />
    </button>
  </div>
);




// Enhanced animations
const style = `
  @keyframes fadeInUp {
    from {
      opacity: 0;
      transform: translateY(20px);
    }
    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @keyframes spin-slow {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes bounce-x {
    0%, 100% {
      transform: translateX(0);
    }
    50% {
      transform: translateX(5px);
    }
  }

  @keyframes bounce-subtle {
    0%, 100% {
      transform: translateY(0);
    }
    50% {
      transform: translateY(-3px);
    }
  }

  .animate-spin-slow {
    animation: spin-slow 10s linear infinite;
  }

  .animate-bounce-x {
    animation: bounce-x 1s infinite;
  }

  .animate-bounce-subtle {
    animation: bounce-subtle 2s infinite;
  }

  .animate-in {
    opacity: 1 !important;
    transform: translateY(0) translateX(0) !important;
  }

  .animate-on-scroll {
    transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
  }
`;

// Add the style to the document head
const styleSheet = document.createElement("style");
styleSheet.innerText = style;
document.head.appendChild(styleSheet);

export default LandingPage;