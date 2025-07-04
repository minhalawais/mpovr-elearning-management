import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { User, Mail, Phone, MapPin, Book, Briefcase, Calendar } from 'lucide-react';
import Navbar from './navbar.tsx';

interface DegreeEntry {
  year: number;
  degree: string;
  institution: string;
}

interface JobEntry {
  years: string;
  company: string;
  position: string;
}

interface Profile {
  user_id: number;
  full_name: string;
  email: string;
  date_of_birth: string | null;
  phone_number: string | null;
  address: string | null;
  education_history: {
    degrees: DegreeEntry[];
  } | null;
  work_experience: {
    jobs: JobEntry[];
  } | null;
  created_at: string;
  updated_at: string;
}

const ViewProfile: React.FC = () => {
  const [profile, setProfile] = useState<Profile | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await fetch('http://localhost:8000/profile', {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
          }
        });
        if (response.ok) {
          const data = await response.json();
          setProfile(data);
        }
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    };

    fetchProfile();
  }, []);

  const renderEducationHistory = (education: Profile['education_history']) => {
    if (!education?.degrees?.length) {
      return <p className="text-gray-500 italic">No education history provided</p>;
    }
    
    return (
      <div className="grid grid-cols-1 gap-4">
        {education.degrees.map((entry, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            key={index}
            className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 border border-purple-100"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-lg font-semibold text-purple-600">{entry.degree}</span>
                <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">
                  {entry.year}
                </span>
              </div>
              <div className="text-gray-600">{entry.institution}</div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  const renderWorkExperience = (experience: Profile['work_experience']) => {
    if (!experience?.jobs?.length) {
      return <p className="text-gray-500 italic">No work experience provided</p>;
    }
    
    return (
      <div className="grid grid-cols-1 gap-4">
        {experience.jobs.map((entry, index) => (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            key={index}
            className="bg-white p-6 rounded-xl shadow-md hover:shadow-lg transition-shadow duration-300 border border-purple-100"
          >
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-lg font-semibold text-purple-600">{entry.position}</span>
                <span className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm">
                  {entry.years}
                </span>
              </div>
              <div className="text-gray-600">{entry.company}</div>
            </div>
          </motion.div>
        ))}
      </div>
    );
  };

  if (!profile) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <>
      <Navbar />
      <div className="min-h-screen bg-gradient-to-b from-purple-50 to-white px-4 py-12 mt-10">
        <div className="max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-2xl shadow-xl p-8 mb-8"
          >
            <div className="flex flex-col md:flex-row items-start md:items-center justify-between mb-8">
              <div className="flex items-center mb-4 md:mb-0">
                <div className="bg-purple-100 p-4 rounded-full mr-4">
                  <User className="w-8 h-8 text-purple-600" />
                </div>
                <div>
                  <h1 className="text-3xl font-bold text-gray-800">{profile.full_name}</h1>
                  <p className="text-gray-500">Trainer Profile</p>
                </div>
              </div>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className="bg-purple-600 text-white px-6 py-2 rounded-full hover:bg-purple-700 transition-colors duration-300 flex items-center space-x-2"
                onClick={() => navigate('/profile/edit')}
              >
                Edit Profile
              </motion.button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
              {[
                { icon: Mail, value: profile.email, label: "Email" },
                { icon: Phone, value: profile.phone_number, label: "Phone" },
                { icon: MapPin, value: profile.address, label: "Address" },
                { icon: Calendar, value: profile.date_of_birth, label: "Date of Birth" }
              ].map((item, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="flex items-start space-x-3 p-4 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors duration-300"
                >
                  <div className="bg-white p-2 rounded-lg shadow-sm">
                    <item.icon className="w-5 h-5 text-purple-600" />
                  </div>
                  <div>
                    <p className="text-sm text-gray-500">{item.label}</p>
                    <p className="text-gray-700">{item.value || 'Not provided'}</p>
                  </div>
                </motion.div>
              ))}
            </div>

            <div className="space-y-8">
              <section>
                <div className="flex items-center mb-6">
                  <div className="bg-purple-100 p-2 rounded-lg mr-3">
                    <Book className="w-5 h-5 text-purple-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-800">Education History</h2>
                </div>
                {renderEducationHistory(profile.education_history)}
              </section>

              <section>
                <div className="flex items-center mb-6">
                  <div className="bg-purple-100 p-2 rounded-lg mr-3">
                    <Briefcase className="w-5 h-5 text-purple-600" />
                  </div>
                  <h2 className="text-2xl font-bold text-gray-800">Work Experience</h2>
                </div>
                {renderWorkExperience(profile.work_experience)}
              </section>
            </div>
          </motion.div>
        </div>
      </div>
    </>
  );
};

export default ViewProfile;

