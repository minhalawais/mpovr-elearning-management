import React, { useEffect } from 'react';
import { ArrowRight, BookOpen, Video, Users, Calendar, Award, MessageSquare, FileCheck, Bell, GraduationCap, ClipboardCheck, Clock, DollarSign, Briefcase, Heart, CheckCircle, Globe, Zap, Trophy } from 'lucide-react';
import TopCoursesSection from './landingPageComponents/courses.tsx'
import StatsSection from './landingPageComponents/statsSection.tsx'
import ProcessSection from './landingPageComponents/processSection.tsx';
import FeaturesSection from './landingPageComponents/featureSection.tsx';
import ProgramTermsSection from './landingPageComponents/programTermsSection.tsx'
import ContactSection from './landingPageComponents/contactSection.tsx';
import Footer from './landingPageComponents/footer.tsx';
import HeroSection from './landingPageComponents/header.tsx';
import FAQSection  from './landingPageComponents/faqSection.tsx';
import theme from "../theme"; // Adjust the path as needed

const LandingPage = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
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

      <FeaturesSection/>

      <TopCoursesSection/>

      <ProcessSection/>

      <ProgramTermsSection/>

      
      <FAQSection/>
      <ContactSection/>

      <Footer/>
    </div>
  );
};






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