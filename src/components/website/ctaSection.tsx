import React from 'react';
import { ArrowRight } from 'lucide-react';

const CTASection: React.FC = () => {
  return (
    <section className="py-24 bg-gradient-to-br from-[#006d77] via-[#3d9299] to-[#83c5be] relative overflow-hidden">
      <div className="absolute inset-0 bg-[url('')] opacity-5"></div>
      <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent"></div>
      <div className="container mx-auto px-6 text-center relative">
        <h2 className="text-5xl font-bold mb-8 text-white">Ready to Transform Your Career?</h2>
        <p className="text-xl mb-12 text-gray-100 max-w-2xl mx-auto">
          Join thousands of successful professionals who took the leap. Your future in IT starts here.
        </p>
        <div className="inline-flex items-center space-x-6">
          <button className="bg-white text-[#006d77] px-8 py-4 rounded-full font-semibold hover:bg-opacity-90 transition-all transform hover:scale-105 shadow-xl hover:shadow-2xl flex items-center group">
            Begin Your Journey
            <ArrowRight className="ml-2 transform group-hover:translate-x-1 transition-transform" />
          </button>
          <button className="border-2 border-white text-white px-8 py-4 rounded-full font-semibold hover:bg-white hover:text-[#006d77] transition-all shadow-lg hover:shadow-xl">
            Learn More
          </button>
        </div>
      </div>
    </section>
  );
};

export default CTASection;
