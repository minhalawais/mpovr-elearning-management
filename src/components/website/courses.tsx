import React from 'react';
import { ArrowRight, BookOpen, Clock, Award, Users } from 'lucide-react';

export default function TopCoursesSection() {
  return (
    <section className="py-24 bg-[#edf6f9] relative overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-b from-white/50 to-transparent"></div>
      <div className="container mx-auto px-6 relative">
        <div className="text-center mb-16">
          <span className="text-[#006d77] bg-[#006d77]/10 px-4 py-2 rounded-full text-sm font-medium">
            Our Top Programs
          </span>
          <h2 className="text-4xl font-bold mt-6 text-[#006d77]">Accelerate Your IT Career</h2>
          <p className="text-xl text-gray-600 mt-4 max-w-2xl mx-auto">
            Choose from our industry-leading courses designed to propel your career to new heights
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <CourseCard
            title="Cloud Computing Mastery"
            description="Master cloud platforms and become a certified cloud architect."
            duration="6 months"
            certifications={['AWS Certified Solutions Architect', 'Azure Administrator']}
            icon={<BookOpen className="w-6 h-6" />}
          />
          <CourseCard
            title="Data Science & AI"
            description="Dive into data analytics, machine learning, and artificial intelligence."
            duration="8 months"
            certifications={['TensorFlow Developer Certificate', 'IBM Data Science Professional']}
            icon={<Users className="w-6 h-6" />}
          />
          <CourseCard
            title="DevOps Engineering"
            description="Learn to streamline development processes and improve deployment efficiency."
            duration="5 months"
            certifications={['Docker Certified Associate', 'Kubernetes Administrator']}
            icon={<Award className="w-6 h-6" />}
          />
        </div>

        <div className="text-center mt-16">
          <button className="bg-[#006d77] text-white px-8 py-4 rounded-full font-semibold hover:bg-[#005a63] transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl inline-flex items-center group">
            Explore All Courses
            <ArrowRight className="ml-2 w-5 h-5 transform group-hover:translate-x-1 transition-transform" />
          </button>
        </div>
      </div>
    </section>
  );
}

interface CourseCardProps {
  title: string;
  description: string;
  duration: string;
  certifications: string[];
  icon: React.ReactNode;
}

const CourseCard: React.FC<CourseCardProps> = ({ title, description, duration, certifications, icon }) => (
  <div className="bg-white rounded-2xl shadow-lg hover:shadow-xl transition-all transform hover:-translate-y-2 overflow-hidden group">
    <div className="p-8">
      <div className="w-16 h-16 bg-[#006d77] text-white rounded-2xl flex items-center justify-center mb-6 transform group-hover:scale-110 transition-transform">
        {icon}
      </div>
      <h3 className="text-2xl font-bold mb-4 text-[#006d77] group-hover:text-[#83c5be] transition-colors">{title}</h3>
      <p className="text-gray-600 mb-6">{description}</p>
      <div className="flex items-center text-[#006d77] mb-4">
        <Clock className="w-5 h-5 mr-2" />
        <span>{duration}</span>
      </div>
      <div className="space-y-2">
        {certifications.map((cert, index) => (
          <div key={index} className="flex items-center text-gray-600">
            <Award className="w-4 h-4 mr-2 text-[#83c5be]" />
            <span className="text-sm">{cert}</span>
          </div>
        ))}
      </div>
    </div>
    <div className="bg-[#edf6f9] p-4 flex justify-between items-center">
      <span className="text-[#006d77] font-semibold">Learn More</span>
      <ArrowRight className="w-5 h-5 text-[#006d77] transform group-hover:translate-x-1 transition-transform" />
    </div>
  </div>
);