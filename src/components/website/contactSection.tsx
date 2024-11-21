import React, { useState } from 'react';
import { Mail, Phone, MapPin, Send, CheckCircle } from 'lucide-react';

const ContactSection: React.FC = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: ''
  });
  const [submitted, setSubmitted] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    // Simulate form submission
    setSubmitted(true);
  };

  if (submitted) {
    return (
      <section className="py-16 bg-[#f4f7f9] relative overflow-hidden">
        <div className="container mx-auto px-6 text-center">
          <div className="max-w-md mx-auto bg-white p-12 rounded-xl shadow-2xl">
            <CheckCircle className="w-24 h-24 mx-auto text-[#399fc6] mb-6" />
            <h2 className="text-3xl font-bold text-[#3756C0] mb-4">Message Sent!</h2>
            <p className="text-gray-600 mb-6">
              We've received your message and will get back to you soon.
            </p>
            <button 
              onClick={() => setSubmitted(false)}
              className="bg-[#E18400] text-white px-8 py-3 rounded-full hover:bg-opacity-90 transition-all"
            >
              Send Another Message
            </button>
          </div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-16 bg-[#f4f7f9] relative">
      <div className="container mx-auto px-6">
        <div className="grid md:grid-cols-2 gap-12 bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Contact Information */}
          <div className="bg-gradient-to-br from-[#3756C0] to-[#399fc6] p-12 text-white flex flex-col justify-center">
            <h2 className="text-4xl font-bold mb-6">Contact Us</h2>
            <p className="text-xl mb-8 opacity-80">
              Have questions about our ERP training? Reach out and our team will be happy to assist you.
            </p>
            
            <div className="space-y-6">
              {[
                { 
                  icon: Mail, 
                  title: 'Email', 
                  content: 'support@mpovr.com' 
                },
                { 
                  icon: Phone, 
                  title: 'Phone', 
                  content: '+1 (555) 123-4567' 
                },
                { 
                  icon: MapPin, 
                  title: 'Address', 
                  content: '123 Tech Lane, Innovation City, CA 94000' 
                }
              ].map((contact, index) => (
                <div key={index} className="flex items-center space-x-4">
                  <contact.icon className="w-8 h-8 text-[#E18400]" />
                  <div>
                    <h4 className="font-semibold">{contact.title}</h4>
                    <p className="opacity-80">{contact.content}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Contact Form */}
          <form onSubmit={handleSubmit} className="p-12 space-y-6">
            <h3 className="text-3xl font-bold text-[#3756C0] mb-6">Get In Touch</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <input 
                type="text" 
                name="name"
                value={formData.name}
                onChange={handleChange}
                placeholder="Your Name"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#399fc6] focus:ring-2 focus:ring-[#399fc6]/30 transition-all"
                required
              />
              <input 
                type="email" 
                name="email"
                value={formData.email}
                onChange={handleChange}
                placeholder="Email Address"
                className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#399fc6] focus:ring-2 focus:ring-[#399fc6]/30 transition-all"
                required
              />
            </div>
            <input 
              type="tel" 
              name="phone"
              value={formData.phone}
              onChange={handleChange}
              placeholder="Phone Number"
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#399fc6] focus:ring-2 focus:ring-[#399fc6]/30 transition-all"
            />
            <textarea 
              name="message"
              value={formData.message}
              onChange={handleChange}
              placeholder="Your Message"
              rows={4}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:border-[#399fc6] focus:ring-2 focus:ring-[#399fc6]/30 transition-all"
              required
            />
            <button 
              type="submit" 
              className="w-full bg-[#E18400] text-white px-6 py-4 rounded-full font-semibold hover:bg-opacity-90 transition-all flex items-center justify-center space-x-2 group"
            >
              <span>Send Message</span>
              <Send className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </button>
          </form>
        </div>
      </div>
    </section>
  );
};

export default ContactSection;